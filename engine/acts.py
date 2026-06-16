"""Sistema de Actos narrativos de PyQuest.

Tres actos + Zona Infinita (∞) que enmarcan la progresión del jugador.
Cada acto tiene un tono narrativo y mecánicas distintas.
"""

from dataclasses import dataclass
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.align import Align
from engine.renderer import console


@dataclass
class Act:
    id: str
    name: str
    subtitle: str
    zone_range: tuple[int, int]
    title_required: str
    color: str
    description: str


ACTS: list[Act] = [
    Act(
        id="I",
        name="El Aprendiz",
        subtitle="Llegas a la ciudad sin poderes",
        zone_range=(1, 4),
        title_required="Aprendiz",
        color="green",
        description=(
            "Llegas a PyQuest City sin conocer sus reglas.\n"
            "Cada calle te enseña los fundamentos: variables, bucles, funciones.\n"
            "El juego te guía con ejemplos, pistas y una red de seguridad."
        ),
    ),
    Act(
        id="II",
        name="El Desarrollador",
        subtitle="Ya entiendes el mundo... pero el mundo te mira",
        zone_range=(5, 9),
        title_required="Dev",
        color="cyan",
        description=(
            "Dominas las herramientas del oficio.\n"
            "Las misiones son más abiertas, menos andamio.\n"
            "Empiezas a ver el engine desde adentro.\n"
            "A veces, el juego te muestra sus propios planos..."
        ),
    ),
    Act(
        id="III",
        name="El Arquitecto",
        subtitle="El código es poder",
        zone_range=(10, 12),
        title_required="Senior",
        color="magenta",
        description=(
            "Has llegado al corazón del engine.\n"
            "El juego te da acceso a los cimientos.\n"
            "Tu misión final no es resolver un reto — es escribir uno."
        ),
    ),
    Act(
        id="∞",
        name="El Creador",
        subtitle="El mundo que escribes",
        zone_range=(13, 999),
        title_required="Legend",
        color="yellow",
        description=(
            "Has desbloqueado la capacidad de crear.\n"
            "Cada zona que escribes se integra al juego.\n"
            "PyQuest crece contigo. El engine nunca sabe cuántas zonas hay."
        ),
    ),
]


def get_act(zone_id: int) -> Act:
    for act in ACTS:
        start, end = act.zone_range
        if start <= zone_id <= end:
            return act
    return ACTS[-1]


def render_act_transition(new_act: Act):
    title = Text()
    title.append(f"\n  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓", style=new_act.color)
    title.append(f"\n  ▓     ACTO {new_act.id}  —  {new_act.name.upper():<20}", style=f"bold {new_act.color}")
    title.append(f"\n  ▓     {new_act.subtitle}", style=f"dim {new_act.color}")
    title.append(f"\n  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓", style=new_act.color)
    console.print(Align.center(title))
    console.print(Panel(Text(new_act.description, style="italic white"), border_style=new_act.color, box=box.ROUNDED, padding=(1, 2)))
    console.input(Align.center(Text("[dim]Presiona Enter para continuar...[/]")))
