"""Task list tests that the fixture format cannot express."""

import mdformat


def test_wrap_accounts_for_checkbox_prefix():
    text = "- [ ] " + "word " * 15
    out = mdformat.text(text, extensions={"myst"}, options={"wrap": 40})
    out_2nd_pass = mdformat.text(out, extensions={"myst"}, options={"wrap": 40})
    assert out == out_2nd_pass
    assert all(len(line) <= 40 for line in out.splitlines())
    assert out.startswith("- [ ] word")


def test_gfm_coexistence(caplog):
    """When mdformat-gfm is enabled too, it must handle task lists
    without renderer conflicts or behavior changes."""
    out = mdformat.text("- [ ] a\n- [x] b\n", extensions={"myst", "gfm"})
    assert out == "- [ ] a\n- [x] b\n"
    assert "conflict" not in caplog.text.lower()


def test_toggle_disabled():
    out = mdformat.text(
        "- [x] done\n",
        extensions={"myst"},
        options={"plugin": {"myst": {"tasklist": False}}},
    )
    assert out == "- [x] done\n"
    # With the toggle off, "[x]" is plain text: a `$`-like MyST escape
    # must not appear and the output must be stable.
    out_2nd_pass = mdformat.text(
        out,
        extensions={"myst"},
        options={"plugin": {"myst": {"tasklist": False}}},
    )
    assert out == out_2nd_pass
