from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Theme:
    name: str
    primary: str = "green"
    secondary: str = "cyan"
    accent: str = "yellow"
    success: str = "green"
    error: str = "red"
    info: str = "blue"
    dim: str = "dim white"
    border: str = "blue"
    highlight_bg: str = "on blue"
    compact: bool = False
    max_width: Optional[int] = None

    def style(self, base: str, bold: bool = False) -> str:
        if bold:
            return f"bold {base}"
        return base


_THEMES: dict[str, Theme] = {}


def register_theme(theme: Theme):
    _THEMES[theme.name] = theme


def get_theme(name: str = "default") -> Theme:
    if name in _THEMES:
        return _THEMES[name]
    if "default" in _THEMES:
        return _THEMES["default"]
    return Theme(name="default")


register_theme(Theme(
    name="default",
    primary="green", secondary="cyan", accent="yellow",
    success="green", error="red", info="blue",
    dim="dim white", border="bright_blue", highlight_bg="on blue",
))

register_theme(Theme(
    name="termux",
    primary="bright_green", secondary="bright_cyan", accent="bright_yellow",
    success="bright_green", error="bright_red", info="bright_blue",
    dim="dim", border="white", highlight_bg="on bright_blue",
    compact=True, max_width=60,
))

register_theme(Theme(
    name="high_contrast",
    primary="white", secondary="yellow", accent="bright_yellow",
    success="green", error="red", info="cyan",
    dim="dim white", border="white", highlight_bg="on white",
    compact=False, max_width=80,
))
