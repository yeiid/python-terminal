from rich.console import Console
from ui.responsive import responsive


def _create_console():
    is_termux = responsive.is_termux
    force_terminal = os.environ.get("FORCE_COLOR") or is_termux

    return Console(
        force_terminal=bool(force_terminal) or None,
        highlight=False,
        color_system="truecolor" if is_termux else "auto",
    )


import os

console = _create_console()
