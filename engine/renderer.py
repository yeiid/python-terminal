from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich import box
from rich.align import Align
from rich.progress_bar import ProgressBar
from engine.state import GameState

console = Console()


def show_title_screen(state: GameState):
    console.clear()
    t = Text()
    t.append("╔══════════════════════════════════════════╗\n", style="bold green")
    t.append("║        ", style="bold green")
    t.append("PyQuest", style="bold yellow")
    t.append(" — Terminal RPG            ", style="bold green")
    t.append("║\n", style="bold green")
    t.append("║   ", style="bold green")
    t.append("Aprende Python como un héroe", style="cyan")
    t.append("     ", style="bold green")
    t.append("║\n", style="bold green")
    t.append("╚══════════════════════════════════════════╝", style="bold green")
    console.print(Align.center(t))

    if not state.player_name or state.player_name == "Dev":
        state.player_name = console.input("[bold]\n¿Cuál es tu nombre, dev? [/]")


def make_header(zone: "Zone", state: GameState, act_name: str = "") -> Panel:
    text = Text()
    text.append(" ⚔️  PyQuest ", style="bold green")
    text.append(f"· {zone.name}  ", style="bold cyan")
    text.append(f"·  Lv.{state.level}  ", style="bold yellow")
    text.append(f"[{state.title}]", style="magenta")
    text.append(f"  🎯{zone.id}/∞" if zone.id >= 13 else f"  🎯{zone.id}/12", style="dim")
    if act_name:
        text.append(f"  [{act_name}]", style="bold white")
    return Panel(text, border_style="bright_blue", box=box.HEAVY)


def render_story(story_text: str):
    panel = Panel(
        Align.left(Text(story_text, style="italic white")),
        border_style="dim white",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    console.print(panel)


def render_mission(
    zone_name: str,
    mission_num: int,
    mission_total: int,
    title: str,
    description: str,
    example: str | None = None,
    xp_reward: int = 0,
):
    header = Text()
    header.append(f"  ▶ MISIÓN {mission_num}/{mission_total}", style="bold yellow")
    header.append(f"  ─  {title}", style="bold white")
    header.append(f"  (+{xp_reward} XP)", style="dim green")
    console.print(Panel(header, border_style="yellow", box=box.SQUARE, padding=(0, 1)))

    console.print(Text(description, style="white"), highlight=True)
    if example:
        example_panel = Panel(
            Text(example, style="dim cyan"),
            title="Ejemplo",
            border_style="dim cyan",
            box=box.ROUNDED,
            padding=(0, 1),
            width=60,
        )
        console.print(example_panel)

    console.print()


def render_meta_moment(zone_id: int, mission_num: int):
    """Momentos meta en Acto II donde el juego muestra su propio código."""
    momentos = {
        6: {
            4: (
                "[bold cyan]╔══════════════════════════════════════════╗\n"
                "║  ENCONTRASTE LOS PLANOS DE LA CIUDAD      ║\n"
                "╚══════════════════════════════════════════╝[/]\n\n"
                "Revisas los archivos del sistema y encuentras esto:\n\n"
                "[dim]  # engine/acts.py[/]\n"
                "[dim]  class Act:[/]\n"
                "[dim]      id: str           # I, II, III, ∞[/]\n"
                "[dim]      name: str         # El Aprendiz...[/]\n"
                "[dim]      zone_range: tuple # (1,4), (5,9)...[/]\n\n"
                "[italic]Alguien construyó esto antes que tú.[/]"
            ),
        },
        8: {
            3: (
                "[bold cyan]╔══════════════════════════════════════════╗\n"
                "║  EL CÓDIGO SE MIRA A SÍ MISMO            ║\n"
                "╚══════════════════════════════════════════╝[/]\n\n"
                "Los decoradores que estás aprendiendo...\n"
                "son los mismos que usa el engine para validar tus misiones:\n\n"
                "[dim]  # engine/validator.py[/]\n"
                "[dim]  def validate(stdout, expected):[/]\n"
                "[dim]      return stdout.strip() == expected.strip()[/]\n\n"
                "[italic]El templo es el código que lo ejecuta.[/]"
            ),
        },
    }
    if zone_id in momentos and mission_num in momentos[zone_id]:
        msg = momentos[zone_id][mission_num]
        console.print(Panel(Text.from_markup(msg), border_style="bold cyan", box=box.DOUBLE, padding=(1, 2)))
        console.input(Align.center(Text("[dim]Presiona Enter para asimilarlo...[/]")))


def render_zone_creator_intro():
    """Mensaje de Zona ∞ cuando el jugador accede al creador."""
    msg = (
        "[bold yellow]╔══════════════════════════════════════════╗\n"
        "║        ZONA ∞ — EL CREADOR              ║\n"
        "╚══════════════════════════════════════════╝[/]\n\n"
        "Has llegado al final del juego base.\n"
        "Pero PyQuest nunca termina.\n\n"
        "A partir de ahora, [bold]tú eres quien construye las zonas[/].\n"
        "El engine descubre automáticamente cualquier archivo\n"
        "[cyan]zone_*.py[/] que coloques en [cyan]world/zones/[/].\n\n"
        "Usa [bold]/crear[/] para generar un template.\n"
        "Usa [bold]/validar[/] para verificar tu zona antes de jugarla.\n"
        "Usa este comando desde la terminal:\n"
        "  [green]python main.py --validate mi_zona.py[/]"
    )
    console.print(Panel(Text.from_markup(msg), border_style="yellow", box=box.HEAVY, padding=(1, 2)))
    console.input(Align.center(Text("[dim]Presiona Enter para comenzar...[/]")))


def render_editor_prompt() -> str:
    console.print()
    console.print("[bold green]  >>> [/]", end="")
    return ""


def render_result(state: GameState, passed: bool, msg: str, xp: int = 0):
    if passed:
        panel = Panel(
            Text(f"  ✓ {msg}  (+{xp} XP)", style="bold green"),
            border_style="green",
            box=box.HEAVY,
            padding=(0, 1),
        )
        console.print(panel)
        pct = state.xp_progress * 100
        bar = ProgressBar(total=state.xp_for_next, completed=state.xp, width=30)
        console.print(f"  [yellow]Lv.{state.level}[/] [cyan]{state.title}[/]  [dim]{state.xp}/{state.xp_for_next} ({pct:.0f}%)[/]")
        console.print(bar)
    else:
        panel = Panel(
            Text(f"  ✗ {msg}", style="bold red"),
            border_style="red",
            box=box.SQUARE,
            padding=(0, 1),
        )
        console.print(panel)


def show_commands():
    table = Table(title="Comandos", box=box.SIMPLE, header_style="bold cyan")
    table.add_column("Comando", style="yellow")
    table.add_column("Acción", style="white")
    table.add_row("/perfil", "Ver tu perfil y medallas")
    table.add_row("/mapa", "Ver el mapa de zonas")
    table.add_row("/acto", "Ver el acto actual")
    table.add_row("/crear", "Generar template de zona (Zona ∞)")
    table.add_row("/validar", "Validar una zona creada por ti")
    table.add_row("/ayuda", "Mostrar esta ayuda")
    table.add_row("/salir", "Guardar y salir")
    console.print(table)
