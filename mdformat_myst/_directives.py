from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
import io
from typing import Any

from markdown_it import MarkdownIt
import mdformat
import mdformat.plugins
from mdformat.renderer import LOGGER, RenderContext, RenderTreeNode
import ruamel.yaml

from mdformat_myst._conf import directive_options_style

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

# Directives whose body is not Markdown. Their content must be kept
# verbatim instead of being recursively formatted as Markdown.
_NON_MARKDOWN_DIRECTIVES = frozenset(
    {
        "{code}",
        "{code-block}",
        "{code-cell}",
        "{eval-rst}",
        "{include}",
        "{literalinclude}",
        "{math}",
        "{mermaid}",
        "{raw}",
    }
)


def longest_consecutive_sequence(seq: str, char: str) -> int:
    """Return length of the longest consecutive sequence of `char` characters
    in string `seq`."""
    assert len(char) == 1
    longest = 0
    current_streak = 0
    for c in seq:
        if c == char:
            current_streak += 1
        else:
            current_streak = 0
        if current_streak > longest:
            longest = current_streak
    return longest


def fence(node: RenderTreeNode, context: RenderContext) -> str:
    """Render fences, colon fences and directives.

    Originally copied from upstream `mdformat` core. Changes compared to
    upstream:
    - call `format_directive_content` when a directive is detected
      (instead of treating the contents as code in that case)
    - render `colon_fence` nodes with `:` as the fence character (and
      use a heuristic to ensure good spacing when recombining those).
    """
    info_str = node.info.strip()
    lang = info_str.split(maxsplit=1)[0] if info_str else ""

    if node.type == "colon_fence":
        fence_char = ":"
    # Info strings of backtick code fences can not contain backticks or tildes.
    # If that is the case, we make a tilde code fence instead.
    elif "`" in info_str or "~" in info_str:
        fence_char = "~"
    else:
        fence_char = "`"

    body = _fence_body(node, context, lang, info_str)

    # The fenced contents must not include as long or longer sequence of
    # `fence_char`s as the fence string itself.
    fence_len = max(3, longest_consecutive_sequence(body, fence_char) + 1)
    fence_str = fence_char * fence_len

    formatted_fence = f"{fence_str}{info_str}\n"
    # Heuristic to ensure child colon fences recombine with a leading
    # blank line for consistency.
    if node.type == "colon_fence" and body.startswith(":::"):
        formatted_fence += "\n"
    formatted_fence += f"{body}{fence_str}"
    return formatted_fence


def _fence_body(
    node: RenderTreeNode, context: RenderContext, lang: str, info_str: str
) -> str:
    """Return the formatted body of a fence or colon fence."""
    unformatted_body = node.content
    is_directive = lang.startswith("{") and lang.endswith("}")
    if is_directive:
        # Only colon fenced directive bodies are Markdown. Backtick
        # fences signal literal content, as do a number of well-known
        # directives whose body is code, RST or similar.
        markdown_body = (
            node.type == "colon_fence" and lang not in _NON_MARKDOWN_DIRECTIVES
        )
        return format_directive_content(
            unformatted_body, context, markdown_body=markdown_body
        )
    # Format the code block using enabled codeformatter funcs
    if lang in context.options.get("codeformatters", {}):
        fmt_func = context.options["codeformatters"][lang]
        try:
            return fmt_func(unformatted_body, info_str)
        except Exception:
            # Swallow exceptions so that formatter errors (e.g. due to
            # invalid code) do not crash mdformat.
            assert node.map is not None, "A fence token must have `map` attribute set"
            LOGGER.warning(
                f"Failed formatting content of a {lang} code block "
                f"(line {node.map[0] + 1} before formatting)"
            )
    return unformatted_body


def format_directive_content(
    raw_content: str, context: RenderContext, *, markdown_body: bool
) -> str:
    unformatted_yaml, content = parse_opts_and_content(raw_content)
    if unformatted_yaml is None and not markdown_body:
        return raw_content
    formatted = ""
    if unformatted_yaml is not None:
        options_block = _format_options(unformatted_yaml, context)
        if options_block is None:
            LOGGER.warning("Invalid YAML in MyST directive options.")
            return raw_content
        formatted += options_block
    if content.strip():
        if markdown_body:
            body = _format_markdown_body(content, context)
            if unformatted_yaml is None and _would_parse_as_options(body):
                # Keep a leading blank line so that body content (e.g. a
                # field list) is not parsed as directive options on reparse.
                body = "\n" + body
            formatted += body
        else:
            formatted += content + "\n"
    if not formatted:
        return ""
    # In both the content-containing case (in which case we might have many terminal
    # newlines in the content) and the options-only case (in which case, we have
    # inserted two newlines above to separate the options from the non-existent content)
    # we want to ensure we end in _exactly_ one newline.
    formatted = formatted.rstrip("\n") + "\n"
    # Unless the last thing in the content is a colon-fence, which for consistency we
    # always add padding to. Literal (non-Markdown) bodies must stay verbatim.
    if markdown_body and formatted.endswith(":::\n"):
        formatted += "\n"
    return formatted


def _format_options(unformatted_yaml: str, context: RenderContext) -> str | None:
    """Format directive options, using the colon syntax by default.

    The "yaml" style (a `---`-delimited YAML block) is used when
    configured via the `directive_options` plugin option, or as a
    fallback when the options cannot be represented in colon syntax.
    Returns None if the options are not valid YAML.
    """
    try:
        parsed = yaml.load(unformatted_yaml)
        dump_stream = io.StringIO()
        yaml.dump(parsed, stream=dump_stream)
    except ruamel.yaml.YAMLError:
        return None
    formatted_yaml = dump_stream.getvalue()

    # Remove the YAML closing tag if added by `ruamel.yaml`
    if formatted_yaml.endswith("\n...\n"):
        formatted_yaml = formatted_yaml[:-4]

    # Convert empty YAML to most concise form
    if formatted_yaml == "null\n":
        formatted_yaml = ""

    if directive_options_style(context.options) == "colon":
        colon_block = _as_colon_options(parsed, formatted_yaml)
        if colon_block is not None:
            return colon_block
    return "---\n" + formatted_yaml + "---\n"


def _as_colon_options(parsed: Any, formatted_yaml: str) -> str | None:
    """Convert a dumped YAML options mapping to `:key: value` lines.

    Returns None when the options cannot be represented in colon syntax
    (non-mapping options, or nested/multi-line values), in which case
    the YAML style must be kept.
    """
    if not formatted_yaml:
        # Empty options are dropped in colon style.
        return ""
    if not isinstance(parsed, Mapping):
        return None
    lines = formatted_yaml.splitlines()
    if len(lines) != len(parsed):
        # Multi-line values, nested structures or comments are present.
        return None
    colon_lines = []
    for line in lines:
        key = line.split(":", 1)[0]
        if line != line.strip() or line.startswith("-") or ":" not in line or not key:
            return None
        colon_lines.append(":" + line)
    return "\n".join(colon_lines) + "\n\n"


def _would_parse_as_options(body: str) -> bool:
    """Return True if `parse_opts_and_content` would interpret the start
    of `body` as directive options."""
    first_line = body.split("\n", 1)[0]
    stripped = first_line.lstrip()
    if stripped.startswith(":") and not stripped.startswith(":::"):
        return True
    return len(first_line) >= 3 and all(c == "-" for c in first_line)


def _format_markdown_body(content: str, context: RenderContext) -> str:
    """Recursively format directive content as Markdown."""
    active_plugins = context.options.get("parser_extension", [])
    # Resolve plugin modules back to their string names, as required by
    # `mdformat.text`.
    extension_names = [
        name
        for name, plugin in mdformat.plugins.PARSER_EXTENSIONS.items()
        if plugin in active_plugins
    ]
    # Trailing newlines (and padding after a trailing nested colon
    # fence) are normalized by `format_directive_content`.
    return mdformat.text(
        content,
        options=context.options.get("mdformat", {}),
        extensions=extension_names,
        codeformatters=list(context.options.get("codeformatters", {})),
    )


def parse_opts_and_content(raw_content: str) -> tuple[str | None, str]:
    if not raw_content:
        return None, raw_content
    lines = raw_content.splitlines()
    line = lines.pop(0)
    yaml_lines = []
    if all(c == "-" for c in line) and len(line) >= 3:
        while lines:
            line = lines.pop(0)
            if all(c == "-" for c in line) and len(line) >= 3:
                break
            yaml_lines.append(line)
    elif line.lstrip().startswith(":") and not line.lstrip().startswith(":::"):
        yaml_lines.append(line.lstrip()[1:])
        while lines:
            stripped = lines[0].lstrip()
            if not stripped.startswith(":") or stripped.startswith(":::"):
                break
            line = lines.pop(0).lstrip()[1:]
            yaml_lines.append(line)
    else:
        return None, raw_content

    first_line_is_empty_but_second_line_isnt = (
        len(lines) >= 2 and not lines[0].strip() and lines[1].strip()
    )
    exactly_one_empty_line = len(lines) == 1 and not lines[0].strip()
    if first_line_is_empty_but_second_line_isnt or exactly_one_empty_line:
        lines.pop(0)

    unformatted_yaml = "\n".join(yaml_lines)
    content = "\n".join(lines)
    return unformatted_yaml, content


def render_fence_html(
    self: MarkdownIt, tokens: Sequence, idx: int, options: Mapping, env: MutableMapping
) -> str:
    return ""
