from ui.themes import register_theme, Theme

register_theme(Theme(
    name="termux",
    primary="bright_green",
    secondary="bright_cyan",
    accent="bright_yellow",
    success="bright_green",
    error="bright_red",
    info="bright_blue",
    dim="dim",
    border="white",
    highlight_bg="on bright_blue",
    compact=True,
    max_width=60,
))
