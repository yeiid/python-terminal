from engine.console import console
from engine.acts import ACTS
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.align import Align


ZONES = [
    {"id": 1, "name": "Barrio Base", "tema": "Variables, tipos, f-strings"},
    {"id": 2, "name": "El Laberinto", "tema": "if/else, loops, comprehensions"},
    {"id": 3, "name": "La Fábrica", "tema": "Funciones, args, kwargs, scope"},
    {"id": 4, "name": "El Mercado", "tema": "Listas, dicts, sets, tuples"},
    {"id": 5, "name": "La Torre", "tema": "OOP, herencia, dunder methods"},
    {"id": 6, "name": "El Puerto", "tema": "Módulos, imports, packages"},
    {"id": 7, "name": "Los Archivos", "tema": "open(), pathlib, JSON, CSV"},
    {"id": 8, "name": "El Templo", "tema": "Decoradores, closures, functools"},
    {"id": 9, "name": "El Río", "tema": "Generators, itertools, yield"},
    {"id": 10, "name": "La Red", "tema": "async/await, aiohttp, concurrencia"},
    {"id": 11, "name": "El Arsenal", "tema": "pytest, unittest, TDD"},
    {"id": 12, "name": "El Cuartel", "tema": "os, argparse, subprocess, requests"},
]

ZONE_ICONS = {
    1: "🏘️", 2: "🌀", 3: "🏭", 4: "🏪", 5: "🏰", 6: "⚓",
    7: "📁", 8: "🏛️", 9: "🌊", 10: "🌐", 11: "⚔️", 12: "🏠",
}

ACT_COLORS = {"I": "green", "II": "cyan", "III": "magenta", "∞": "yellow"}


def get_act_label(zone_id: int) -> str:
    for act in ACTS:
        start, end = act.zone_range
        if start <= zone_id <= end:
            return act.id
    return "∞"


def show_map(unlocked_zone: int):
    console.print()
    title = Text("🗺️  Mapa de PyQuest City", style="bold cyan")
    console.print(Align.center(title))

    table = Table(box=box.HEAVY_EDGE, show_header=True, header_style="bold cyan", border_style="blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Acto", width=5)
    table.add_column("Icono", width=4)
    table.add_column("Zona", style="white", width=18)
    table.add_column("Tema", style="dim white", width=38)
    table.add_column("Estado", style="bold", width=12)

    for z in ZONES:
        icon = ZONE_ICONS.get(z["id"], "⬜")
        act = get_act_label(z["id"])
        act_color = ACT_COLORS.get(act, "white")

        if z["id"] < unlocked_zone:
            status = "✓ Completada"
            row_style = "green"
        elif z["id"] == unlocked_zone:
            status = "▶ Actual"
            row_style = "bold yellow"
        else:
            status = "🔒 Bloqueada"
            row_style = "dim"

        table.add_row(
            str(z["id"]),
            f"[{act_color}]Acto {act}[/]",
            icon, z["name"], z["tema"], status,
            style=row_style,
        )

    if unlocked_zone > 12:
        table.add_row(
            "∞",
            "[yellow]Acto ∞[/]",
            "✨",
            "Zona del Creador",
            "Tu propia zona Python",
            "▶ Actual" if unlocked_zone == 13 else "✓ Creada",
            style="bold yellow",
        )

    console.print(table)

    legend = Text()
    for act in ACTS:
        color = ACT_COLORS.get(act.id, "white")
        legend.append(f" [{color}]■ Acto {act.id}: {act.name}[/]  ")
    console.print(Align.center(legend))
    console.print()


def get_zone(zone_id: int):
    for z in ZONES:
        if z["id"] == zone_id:
            return z
    if zone_id > 12:
        return {"id": zone_id, "name": "Zona ∞", "tema": "Tu propia zona"}
    return None
