"""Task list support, adapted from `mdformat-gfm`.

Instead of overriding the `list_item` renderer like `mdformat-gfm` does
(which would conflict with it when both plugins are enabled), a
markdown-it core rule replaces the `html_inline` checkbox injected by
`tasklists_plugin` with a dedicated `myst_task_checkbox` inline token
that has its own renderer. When `mdformat-gfm` is enabled it takes
precedence and this module's hooks turn themselves off.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
import re
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token
import mdformat.plugins
from mdformat.renderer import RenderContext, RenderTreeNode

from mdformat_myst._conf import syntax_enabled

_CHECKBOX_PREFIX = '<input class="task-list-item-checkbox"'
# Same escaped rendition as `mdformat-gfm` so that output does not
# depend on which of the two plugins performs the escaping.
_TODO_PATTERN = re.compile(r"^\[([ xX])\]")


def _gfm_is_active(options: Mapping[str, Any]) -> bool:
    gfm_plugin = mdformat.plugins.PARSER_EXTENSIONS.get("gfm")
    return gfm_plugin is not None and gfm_plugin in options.get("parser_extension", [])


def _normalize_tasklist_tokens(state: StateCore) -> None:
    """Replace `html_inline` checkboxes with `myst_task_checkbox` tokens.

    No-op when `mdformat-gfm` is enabled, so its `list_item` renderer
    handles task lists unchanged.
    """
    if _gfm_is_active(state.md.options):
        return
    for token in state.tokens:
        if token.type != "inline" or not token.children:
            continue
        first_child = token.children[0]
        if first_child.type == "html_inline" and first_child.content.startswith(
            _CHECKBOX_PREFIX
        ):
            checkbox = Token("myst_task_checkbox", "", 0)
            # Keep the original HTML for the HTML render rule below.
            checkbox.content = first_child.content
            checkbox.meta = {"checked": 'checked="checked"' in first_child.content}
            token.children[0] = checkbox


def _render_checkbox_html(
    self: MarkdownIt, tokens: Sequence, idx: int, options: Mapping, env: MutableMapping
) -> str:
    return str(tokens[idx].content)


def update_mdit_tasklists(mdit: MarkdownIt) -> None:
    from mdit_py_plugins.tasklists import tasklists_plugin

    mdit.use(tasklists_plugin)
    mdit.core.ruler.after(
        "github-tasklists", "myst_tasklists_normalize", _normalize_tasklist_tokens
    )
    # Render the original checkbox HTML verbatim so that `mdformat`s AST
    # validation sees output identical to the unmodified plugin's.
    mdit.add_render_rule("myst_task_checkbox", _render_checkbox_html)


def task_checkbox_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return "[x]" if node.meta["checked"] else "[ ]"


def escape_tasklist_paragraph(
    text: str, node: RenderTreeNode, context: RenderContext
) -> str:
    """Escape a literal leading "[x]" in the first paragraph of a list
    item so that it does not turn into a task list item on reparse."""
    if not syntax_enabled(context.options, "tasklist"):
        return text
    if _gfm_is_active(context.options):
        # mdformat-gfm escapes task-list-lookalikes itself.
        return text
    if not (node.parent and node.parent.type == "list_item"):
        return text
    if node.previous_sibling is not None:
        return text
    inline_node = node.children[0]
    if inline_node.children and inline_node.children[0].type == "myst_task_checkbox":
        # A real checkbox; must not be escaped.
        return text
    first_line, newline, rest = text.partition("\n")
    first_line = _TODO_PATTERN.sub(r"\\[\g<1>\\]", first_line)
    return first_line + newline + rest
