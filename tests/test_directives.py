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


AUTOMODULE = """:::{automodule} mymodule
:members:

.. rubric:: Details
   with indented RST
:::
"""


def test_automodule_body_is_literal_by_default():
    out = mdformat.text(AUTOMODULE, extensions={"myst"}, options={"wrap": 70})
    assert out == AUTOMODULE


CUSTOM = """:::{my-list}
entry_one
entry_two
:::
"""


def test_configured_literal_directive_via_api():
    opts = {"wrap": 70, "plugin": {"myst": {"literal_directives": ["my-list"]}}}
    out = mdformat.text(CUSTOM, extensions={"myst"}, options=opts)
    assert out == CUSTOM
    # Without the config the body is Markdown and gets reflowed.
    out = mdformat.text(CUSTOM, extensions={"myst"}, options={"wrap": 70})
    assert out == ":::{my-list}\nentry_one entry_two\n:::\n"


def test_configured_literal_directive_via_cli(tmp_path):
    import mdformat._cli

    file_path = tmp_path / "test_markdown.md"
    file_path.write_text(CUSTOM)
    assert (
        mdformat._cli.run(
            ["--wrap=70", "--myst-literal-directives", "my-list,other", str(file_path)]
        )
        == 0
    )
    assert file_path.read_text() == CUSTOM


def test_markdown_directive_body_is_wrapped():
    """Regular directive bodies are Markdown and do wrap."""
    src = ":::{note}\n" + "word " * 30 + "\n:::\n"
    out = mdformat.text(src, extensions={"myst"}, options={"wrap": 40})
    body_lines = out.splitlines()[1:-1]
    assert len(body_lines) > 1
    assert all(len(line) <= 40 for line in body_lines)
