from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
import io
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.token import Token
import mdformat
from mdformat._util import build_mdit
import mdformat.plugins
from mdformat.renderer import LOGGER, MDRenderer, RenderContext, RenderTreeNode
import ruamel.yaml

from mdformat_myst._conf import directive_options_style

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
# Never fold long scalars onto multiple lines: folding would make long
# option values appear unrepresentable in colon syntax, and mdformat
# never wraps fence contents anyway.
yaml.width = 100_000

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

# Parser used to find reference-style links inside MyST directive bodies.
# Directives are tokenized as fences, so mdformat would otherwise treat those
# links as unused and drop their definitions.
_DIRECTIVE_REF_PARSER = MarkdownIt("commonmark")
_DIRECTIVE_REF_PARSER.options["store_labels"] = True


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
      (instead of treating the contents as code in that case), and
      record link references used only inside the directive body
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
        mark_refs_used_in_directive(unformatted_body, context)
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


def _is_myst_directive(info_str: str) -> bool:
    lang = info_str.split(maxsplit=1)[0] if info_str.strip() else ""
    return lang.startswith("{") and lang.endswith("}")


def mark_refs_used_in_directive(raw_content: str, context: RenderContext) -> None:
    """Keep link/image refs that are only referenced inside a directive."""
    references = context.env.get("references")
    used_refs = context.env.get("used_refs")
    if not raw_content or not references or used_refs is None:
        return
    _collect_refs_from_markdown(raw_content, references, used_refs)


def _collect_refs_from_markdown(
    content: str,
    references: Mapping[str, object],
    used_refs: set[str],
) -> None:
    env: dict = {"references": dict(references)}
    tokens = _DIRECTIVE_REF_PARSER.parse(content, env)
    _collect_ref_labels(tokens, references, used_refs)


def _collect_ref_labels(
    tokens: Sequence[Token],
    references: Mapping[str, object],
    used_refs: set[str],
) -> None:
    for token in tokens:
        if token.type in ("link_open", "image"):
            label = token.meta.get("label") if token.meta else None
            if isinstance(label, str) and label in references:
                used_refs.add(label)
        elif token.type == "fence" and token.content and _is_myst_directive(token.info):
            _collect_refs_from_markdown(token.content, references, used_refs)
        if token.children:
            _collect_ref_labels(token.children, references, used_refs)


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
    """Recursively format directive content as Markdown.

    The nested render is seeded with the outer document's link reference
    definitions so that reference links keep working inside directive
    bodies. References used (or defined) in the body are merged into the
    outer document's environment, whose finalization emits each
    definition once, at the end of the document.

    Trailing newlines (and padding after a trailing nested colon fence)
    are normalized by `format_directive_content`.
    """
    active_plugins = context.options.get("parser_extension", [])
    # Resolve plugin modules back to their string names, as required by
    # `build_mdit`.
    extension_names = [
        name
        for name, plugin in mdformat.plugins.PARSER_EXTENSIONS.items()
        if plugin in active_plugins
    ]
    mdformat_opts = context.options.get("mdformat", {})
    mdit = build_mdit(
        MDRenderer,
        mdformat_opts=mdformat_opts,
        extensions=extension_names,
        codeformatters=set(context.options.get("codeformatters", {})),
    )

    renderer = mdit.renderer
    assert isinstance(renderer, MDRenderer)

    def render_pass(src: str, references: Mapping[str, Any]) -> tuple[str, dict]:
        env: dict = {"references": dict(references)}
        tokens = mdit.parse(src, env)
        text = renderer.render(tokens, mdit.options, env, finalize=False)
        return text, env

    formatted, env = render_pass(content, context.env.get("references", {}))
    # Mimic `mdformat.text`: if word wrap is changed, add a second
    # rendering pass to achieve stable formatting.
    if mdformat_opts.get("wrap", "keep") != "keep":
        formatted, env = render_pass(formatted, env["references"])

    # Merge references used or defined in the body into the outer document.
    outer_references = context.env.setdefault("references", {})
    for label, ref in env["references"].items():
        outer_references.setdefault(label, ref)
    context.env.setdefault("used_refs", set()).update(env["used_refs"])
    return formatted


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
