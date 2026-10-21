"""Field list rendering (`:name: body` syntax)."""

from __future__ import annotations

import re
import textwrap

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode

from mdformat_myst._conf import syntax_enabled

_BODY_INDENT = 2
# A line that would parse as a field name marker: a colon, a name of
# non-colon characters containing at least one non-whitespace character,
# and a closing colon.
_FIELD_MARKER_PATTERN = re.compile(r"^:[^:\n]*[^\s:][^:\n]*:")


def update_mdit_fieldlist(mdit: MarkdownIt) -> None:
    from mdit_py_plugins.field_list import fieldlist_plugin

    mdit.use(fieldlist_plugin)


def render_fieldlist_name(node: RenderTreeNode, context: RenderContext) -> str:
    return ":" + node.children[0].render(context) + ":"


def render_fieldlist_body(node: RenderTreeNode, context: RenderContext) -> str:
    with context.indented(_BODY_INDENT):
        rendered = "\n\n".join(child.render(context) for child in node.children)
    return textwrap.indent(
        rendered, " " * _BODY_INDENT, lambda line: bool(line.strip())
    )


def render_field_list(node: RenderTreeNode, context: RenderContext) -> str:
    entries = []
    name = ""
    for child in node.children:
        if child.type == "fieldlist_name":
            name = child.render(context)
            continue
        assert child.type == "fieldlist_body"
        body = child.render(context)
        if not body:
            entries.append(name)
        elif child.children[0].type == "paragraph":
            # Put the first body line on the marker line (the common
            # `:param x: description` style).
            first_line, newline, rest = body.partition("\n")
            entries.append(f"{name} {first_line.strip()}{newline}{rest}")
        else:
            # A body starting with a non-paragraph block (fence, list,
            # ...) must keep its own indent, below the marker line.
            entries.append(f"{name}\n{body}")
    return "\n".join(entries)


def escape_fieldlist_paragraph(
    text: str, node: RenderTreeNode, context: RenderContext
) -> str:
    """Escape paragraph lines that would otherwise be parsed as field
    name markers (field lists may interrupt paragraphs)."""
    if not syntax_enabled(context.options, "fieldlist"):
        return text
    return "\n".join(
        "\\" + line if _FIELD_MARKER_PATTERN.match(line) else line
        for line in text.split("\n")
    )
