"""Menú con tabs navegable con Tab para PyQuest.

Usa prompt_toolkit para capturar Tab/Enter y navegar entre opciones.
Cada tab es un "botón" que al seleccionarlo ejecuta una acción.
"""

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich import box


class TabMenu:
    """Menú de tabs horizontales navegable con Tab y Enter."""

    def __init__(self, title: str, tabs: list[dict]):
        """
        tabs: list of {"label": str, "action": callable, "icon": str}
        """
        self.title = title
        self.tabs = tabs
        self.selected = 0

    def render(self) -> str:
        """Renderiza los tabs y retorna HTML-like string."""
        lines = []
        lines.append(f"\n  {self.title}\n")
        for i, tab in enumerate(self.tabs):
            icon = tab.get("icon", " ")
            label = tab["label"]
            if i == self.selected:
                lines.append(f"  ┌{'─' * (len(label) + 4)}┐")
                lines.append(f"  │ {icon} [{label}] │◄")
                lines.append(f"  └{'─' * (len(label) + 4)}┘")
            else:
                lines.append(f"    {icon}  {label}")
        lines.append("\n  [Tab] Navegar  [Enter] Seleccionar  [Esc] Volver")
        return "\n".join(lines)

    def run(self) -> str:
        """Ejecuta el menú con navegación por Tab. Retorna label seleccionado."""
        kb = KeyBindings()

        @kb.add(keys=Keys.Tab)
        def _(event):
            self.selected = (self.selected + 1) % len(self.tabs)

        @kb.add(keys=Keys.BackTab)
        def _(event):
            self.selected = (self.selected - 1) % len(self.tabs)

        result = [None]

        @kb.add(keys=Keys.Enter)
        def _(event):
            result[0] = self.tabs[self.selected]["label"]
            event.app.exit()

        @kb.add(keys=Keys.Escape)
        def _(event):
            event.app.exit()

        session = PromptSession()
        try:
            session.prompt(
                self.render,
                key_bindings=kb,
                mouse_support=False,
            )
        except (EOFError, KeyboardInterrupt):
            pass

        return result[0]


def render_tab_bar(tabs: list[dict], active_idx: int) -> Panel:
    """Renderiza barra de tabs horizontal con el activo resaltado."""
    table = Table.grid(padding=(0, 1))
    parts = []
    for i, tab in enumerate(tabs):
        icon = tab.get("icon", " ")
        label = tab["label"]
        if i == active_idx:
            parts.append(f"  [bold white on blue] {icon} {label} [/]  ")
        else:
            parts.append(f"  [dim]{icon} {label}[/]  ")
    table.add_row("".join(parts))
    return Panel(table, border_style="blue", box=box.SIMPLE, padding=(0, 0))
