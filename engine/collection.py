"""Sistema de colección de objetos de código — uno por zona, requiere 3+ misiones."""

from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box
from rich.align import Align
from engine.console import console
from engine.battlepass import COLLECTION_OBJECTS


def check_zone_object_unlocked(
    zone_id: int,
    completed_missions: list[str],
    collected_objects: list[str],
) -> bool:
    obj = _get_obj_for_zone(zone_id)
    if not obj:
        return False
    if obj["id"] in collected_objects:
        return True
    zone_missions = [m for m in completed_missions if m.startswith(f"{zone_id}-")]
    return len(zone_missions) >= 3


def try_collect_object(
    zone_id: int,
    completed_missions: list[str],
    collected_objects: list[str],
) -> str | None:
    obj = _get_obj_for_zone(zone_id)
    if not obj:
        return None
    if obj["id"] in collected_objects:
        return None
    zone_missions = [m for m in completed_missions if m.startswith(f"{zone_id}-")]
    if len(zone_missions) >= 3:
        collected_objects.append(obj["id"])
        return obj["name"]
    return None


def _get_obj_for_zone(zone_id: int) -> dict | None:
    for obj in COLLECTION_OBJECTS:
        if obj["zone_id"] == zone_id:
            return obj
    return None


def render_collection(collected_objects: list[str]):
    total = len(COLLECTION_OBJECTS)
    unlocked_count = len(collected_objects)
    pct = (unlocked_count / total) * 100 if total else 0

    console.print(Text(f"  💠 COLECCIÓN DE CÓDIGO  —  {unlocked_count}/{total} ({pct:.0f}%)", style="bold cyan"))
    console.print()

    table = Table.grid(padding=(0, 2))
    for obj in COLLECTION_OBJECTS:
        have = obj["id"] in collected_objects
        icon = obj["icon"] if have else "🔒"
        name = f"[bold green]{obj['name']}[/]" if have else f"[dim]{obj['name']}[/]"
        desc = obj["desc"] if have else "???"
        desc_style = "dim white" if have else "dim"
        status = "[green]✓[/]" if have else f"[dim]Zona {obj['zone_id']}[/]"
        table.add_row(f"  {icon}", name, f"[{desc_style}]{desc}[/]", status)

    console.print(Panel(table, border_style="cyan", box=box.SIMPLE, padding=(0, 1)))
