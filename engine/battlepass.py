"""Battle Pass / Pase de Nivel — progresión por XP total ganado."""

from dataclasses import dataclass, field
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress_bar import ProgressBar
from rich import box
from rich.align import Align
from engine.console import console


BATTLE_PASS_TIERS = [
    {"tier": 1,  "xp_needed": 0,    "reward": "Título: Aprendiz",           "icon": "🌱"},
    {"tier": 2,  "xp_needed": 200,  "reward": "Título: Dev",               "icon": "⚙️"},
    {"tier": 3,  "xp_needed": 500,  "reward": "Badge: Primer Código",       "icon": "📜"},
    {"tier": 4,  "xp_needed": 1000, "reward": "Título: Coder",              "icon": "💻"},
    {"tier": 5,  "xp_needed": 1500, "reward": "Badge: Velocista",           "icon": "⚡"},
    {"tier": 6,  "xp_needed": 2000, "reward": "Título: Ninja",              "icon": "🥷"},
    {"tier": 7,  "xp_needed": 3000, "reward": "Badge: Depurador",           "icon": "🐛"},
    {"tier": 8,  "xp_needed": 4000, "reward": "Título: Arquitecto",         "icon": "🏛️"},
    {"tier": 9,  "xp_needed": 5000, "reward": "Badge: Legendario",          "icon": "💎"},
    {"tier": 10, "xp_needed": 7000, "reward": "Título: Legend + Skin Élite","icon": "👑"},
]

COLLECTION_OBJECTS = [
    {"id": "obj_01", "name": "Variable Espectral",      "zone_id": 1,  "icon": "🔮", "desc": "El primer fragmento de código vivo"},
    {"id": "obj_02", "name": "Bucle Infinito",           "zone_id": 2,  "icon": "🌀", "desc": "Un loop que nunca debió romperse"},
    {"id": "obj_03", "name": "Función Olvidada",         "zone_id": 3,  "icon": "⚙️", "desc": "Una función sin nombre en la memoria"},
    {"id": "obj_04", "name": "Estructura de Datos Viva", "zone_id": 4,  "icon": "🗃️", "desc": "Un dict que respira"},
    {"id": "obj_05", "name": "Objeto Encapsulado",       "zone_id": 5,  "icon": "📦", "desc": "Herencia de una era pasada"},
    {"id": "obj_06", "name": "Módulo Perdido",           "zone_id": 6,  "icon": "📦", "desc": "Un import sin destino"},
    {"id": "obj_07", "name": "Archivo Corrupto",         "zone_id": 7,  "icon": "📄", "desc": "Datos que no deberían existir"},
    {"id": "obj_08", "name": "Decorador Ancestral",      "zone_id": 8,  "icon": "🎭", "desc": "Un @ que cambia la realidad"},
    {"id": "obj_09", "name": "Generador Eterno",         "zone_id": 9,  "icon": "♻️", "desc": "Un yield sin fin"},
    {"id": "obj_10", "name": "Promesa Asíncrona",        "zone_id": 10, "icon": "⏳", "desc": "Un await que nunca llegó"},
    {"id": "obj_11", "name": "Test Fantasma",            "zone_id": 11, "icon": "👻", "desc": "Un assertion que falla en otra dimensión"},
    {"id": "obj_12", "name": "Comando Raíz",             "zone_id": 12, "icon": "⚡", "desc": "El poder del sistema operativo"},
    {"id": "obj_13", "name": "Excepción Primordial",     "zone_id": 13, "icon": "🔥", "desc": "El error que inició todo"},
    {"id": "obj_14", "name": "Contexto Dimensional",     "zone_id": 14, "icon": "🌌", "desc": "Un portal de entrada y salida"},
    {"id": "obj_15", "name": "Datos del Origen",         "zone_id": 15, "icon": "💾", "desc": "La memoria del mundo"},
]


def get_battle_pass_tier(total_xp: int) -> int:
    tier = 0
    for t in BATTLE_PASS_TIERS:
        if total_xp >= t["xp_needed"]:
            tier = t["tier"]
    return tier


def get_next_tier_info(total_xp: int) -> tuple[int | None, int, int]:
    for t in BATTLE_PASS_TIERS:
        if total_xp < t["xp_needed"]:
            return t["tier"], t["xp_needed"] - total_xp, t["xp_needed"]
    return None, 0, BATTLE_PASS_TIERS[-1]["xp_needed"]


def get_tiers_up_to(total_xp: int) -> list[dict]:
    result = []
    for t in BATTLE_PASS_TIERS:
        result.append({**t, "unlocked": total_xp >= t["xp_needed"]})
    return result


def render_battle_pass(total_xp: int):
    current_tier = get_battle_pass_tier(total_xp)
    next_tier, xp_remaining, xp_next_needed = get_next_tier_info(total_xp)

    title = Text(f"  🏆 PASE DE BATALLA  —  Nivel {current_tier}/10", style="bold yellow")
    console.print(Align.center(title))

    if next_tier:
        bar = ProgressBar(total=xp_next_needed, completed=total_xp, width=40)
        pct = (total_xp / xp_next_needed) * 100
        console.print(f"  XP Total: {total_xp}  —  Siguiente nivel: +{xp_remaining} XP")
        console.print(bar)
    else:
        console.print(f"  [bold green]✓ PASE COMPLETADO[/]  —  XP Total: {total_xp}")

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan")
    table.add_column("Nivel", width=6)
    table.add_column("XP Necesaria", width=14)
    table.add_column("Recompensa", width=30)
    table.add_column("Estado", width=12)

    for t in reversed(get_tiers_up_to(total_xp)):
        if t["unlocked"]:
            status = "✓ Desbloqueado"
            style = "green"
        elif next_tier and t["tier"] == next_tier:
            status = "▶ En progreso"
            style = "yellow"
        else:
            status = "🔒 Bloqueado"
            style = "dim"
        table.add_row(
            f"{t['icon']} {t['tier']}",
            str(t["xp_needed"]),
            t["reward"],
            f"[{style}]{status}[/]",
            style=style,
        )

    console.print(table)


def get_collectible_for_zone(zone_id: int) -> dict | None:
    for obj in COLLECTION_OBJECTS:
        if obj["zone_id"] == zone_id:
            return obj
    return None
