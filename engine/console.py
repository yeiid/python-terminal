from rich.console import Console
import os


def _create_console():
    is_termux = "TERMUX_VERSION" in os.environ
    force_terminal = os.environ.get("FORCE_COLOR") or is_termux

    return Console(
        force_terminal=bool(force_terminal) or None,
        highlight=False,
        color_system="truecolor" if is_termux else "auto",
    )


console = _create_console()
