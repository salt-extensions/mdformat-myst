"""Directive body tests that the fixture format cannot express."""

import mdformat

TOCTREE = """:::{toctree}
:hidden:
:maxdepth: 1

quickstart_token
quickstart_approle
quickstart_local
:::
"""


def test_toctree_body_is_not_reflowed():
    """A toctree body is a list of documents, one per line, not a
    Markdown paragraph: word wrap must never join the lines."""
    out = mdformat.text(TOCTREE, extensions={"myst"}, options={"wrap": 70})
    assert out == TOCTREE
    out_2nd_pass = mdformat.text(out, extensions={"myst"}, options={"wrap": 70})
    assert out == out_2nd_pass


def test_markdown_directive_body_is_wrapped():
    """Regular directive bodies are Markdown and do wrap."""
    src = ":::{note}\n" + "word " * 30 + "\n:::\n"
    out = mdformat.text(src, extensions={"myst"}, options={"wrap": 40})
    body_lines = out.splitlines()[1:-1]
    assert len(body_lines) > 1
    assert all(len(line) <= 40 for line in body_lines)
