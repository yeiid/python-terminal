"""Sistema de Actos narrativos y mecánicos de PyQuest.

Cada Acto cambia no solo la narrativa sino también las reglas del juego:
- Acto I: máximo soporte (hints ilimitados, code_template siempre presente)
- Acto II: menos soporte (hints limitados, code_template opcional)
- Acto III: mínima ayuda (sin hints, sin code_template)
- Acto ∞: el jugador es el creador
"""

from dataclasses import dataclass
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.align import Align
from engine.console import console


@dataclass
class Act:
    id: str
    name: str
    subtitle: str
    zone_range: tuple[int, int]
    color: str
    description: str
    max_hints_per_mission: int    # -1 = ilimitados
    code_template_required: bool  # True = siempre debe existir
    allow_skip_with_penalty: bool
    xp_multiplier: float          # 1.0 en Acto I, 1.5 en II, 2.0 en III


ACTS: list[Act] = [
    Act(
        id="I",
        name="El Aprendiz",
        subtitle="Llegas a la ciudad sin poderes",
        zone_range=(1, 4),
        color="green",
        description=(
            "Llegas a PyQuest City sin conocer sus reglas.\n"
            "Cada calle te enseña los fundamentos: variables, bucles, funciones.\n"
            "El juego te guía con ejemplos, pistas ilimitadas y una red de seguridad."
        ),
        max_hints_per_mission=-1,
        code_template_required=True,
        allow_skip_with_penalty=True,
        xp_multiplier=1.0,
    ),
    Act(
        id="II",
        name="El Desarrollador",
        subtitle="Ya entiendes el mundo... pero el mundo te mira",
        zone_range=(5, 9),
        color="cyan",
        description=(
            "Dominas las herramientas del oficio.\n"
            "Las misiones son más abiertas, menos andamio.\n"
            "Empiezas a ver el engine desde adentro.\n"
            "A veces, el juego te muestra sus propios planos...\n\n"
            "[dim]Límite: 3 pistas por misión. Código base opcional.[/]"
        ),
        max_hints_per_mission=3,
        code_template_required=False,
        allow_skip_with_penalty=True,
        xp_multiplier=1.5,
    ),
    Act(
        id="III",
        name="El Arquitecto",
        subtitle="El código es poder",
        zone_range=(10, 12),
        color="magenta",
        description=(
            "Has llegado al corazón del engine.\n"
            "Sin pistas. Sin código base. Solo tú y el problema.\n"
            "Tu misión final no es resolver un reto — es escribir uno."
        ),
        max_hints_per_mission=0,
        code_template_required=False,
        allow_skip_with_penalty=False,
        xp_multiplier=2.0,
    ),
    Act(
        id="∞",
        name="El Creador",
        subtitle="El mundo que escribes",
        zone_range=(13, 999),
        color="yellow",
        description=(
            "Has desbloqueado la capacidad de crear.\n"
            "Cada zona que escribes se integra al juego.\n"
            "PyQuest crece contigo. El engine nunca sabe cuántas zonas hay."
        ),
        max_hints_per_mission=-1,
        code_template_required=False,
        allow_skip_with_penalty=False,
        xp_multiplier=3.0,
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
    console.print(Panel(Text.from_markup(new_act.description), border_style=new_act.color, box=box.ROUNDED, padding=(1, 2)))
    console.input(Align.center(Text("[dim]Presiona Enter para continuar...[/]")))
