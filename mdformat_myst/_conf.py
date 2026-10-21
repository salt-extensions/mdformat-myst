from __future__ import annotations

from collections.abc import Mapping
from typing import Any

SYNTAX_TOGGLES = ("colon_fence", "deflist", "tasklist", "fieldlist")


def directive_options_style(options: Mapping[str, Any]) -> str:
    """Read the directive options style: "colon" (default) or "yaml"."""
    plugin_conf = options.get("mdformat", {}).get("plugin", {}).get("myst", {})
    return str(plugin_conf.get("directive_options", "colon"))


def syntax_enabled(options: Mapping[str, Any], name: str) -> bool:
    """Read a mdformat-myst syntax extension toggle (default: enabled).

    `options` is the markdown-it options mapping (`mdit.options` /
    `RenderContext.options`). Toggle values come from the
    `[plugin.myst]` TOML section or the corresponding CLI flags.
    """
    plugin_conf = options.get("mdformat", {}).get("plugin", {}).get("myst", {})
    return bool(plugin_conf.get(name, True))
