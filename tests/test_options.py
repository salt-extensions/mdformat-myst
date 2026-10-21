"""Tests for the `[plugin.myst]` syntax extension toggles."""

import mdformat
import mdformat._cli

COLON_FENCE_INPUT = ":::{note}\nA note.\n:::\n"
# With `colon_fence` enabled (the default) the input is valid MyST
# syntax and must be preserved as is.
COLON_FENCE_ENABLED_OUTPUT = COLON_FENCE_INPUT
# With `colon_fence` disabled the input is a plain paragraph whose
# role-like `{note}` part gets escaped (the pre-toggle behavior).
COLON_FENCE_DISABLED_OUTPUT = ":::\\{note}\nA note.\n:::\n"


def test_toggle_default_enabled():
    assert (
        mdformat.text(COLON_FENCE_INPUT, extensions={"myst"})
        == COLON_FENCE_ENABLED_OUTPUT
    )


def test_toggle_disabled_via_api():
    assert (
        mdformat.text(
            COLON_FENCE_INPUT,
            extensions={"myst"},
            options={"plugin": {"myst": {"colon_fence": False}}},
        )
        == COLON_FENCE_DISABLED_OUTPUT
    )


def test_toggle_disabled_via_cli_flag(tmp_path):
    file_path = tmp_path / "test_markdown.md"
    file_path.write_text(COLON_FENCE_INPUT)
    assert mdformat._cli.run(["--myst-no-colon-fence", str(file_path)]) == 0
    assert file_path.read_text() == COLON_FENCE_DISABLED_OUTPUT


def test_toggle_disabled_via_toml(tmp_path):
    (tmp_path / ".mdformat.toml").write_text("[plugin.myst]\ncolon_fence = false\n")
    file_path = tmp_path / "test_markdown.md"
    file_path.write_text(COLON_FENCE_INPUT)
    assert mdformat._cli.run([str(file_path)]) == 0
    assert file_path.read_text() == COLON_FENCE_DISABLED_OUTPUT


def test_cli_flag_overrides_toml(tmp_path):
    """A CLI disable flag wins; an absent flag defers to TOML."""
    (tmp_path / ".mdformat.toml").write_text("[plugin.myst]\ntasklist = false\n")
    file_path = tmp_path / "test_markdown.md"
    file_path.write_text(COLON_FENCE_INPUT)
    assert mdformat._cli.run(["--myst-no-colon-fence", str(file_path)]) == 0
    assert file_path.read_text() == COLON_FENCE_DISABLED_OUTPUT
