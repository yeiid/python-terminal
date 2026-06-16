import time
import random
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich import box
from rich.align import Align
from rich.progress_bar import ProgressBar
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, BarColumn, TextColumn
from engine.state import GameState
from engine.acts import Act
from engine.console import console


def type_print(text: str, delay: float = 0.015, style: str = ""):
    """Typing effect para narrativa. No usar en feedback técnico."""
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(delay)
    console.print()


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


def make_header(zone: "Zone", state: GameState, act: Act | None = None) -> Panel:
    text = Text()
    text.append(" ⚔️  PyQuest ", style="bold green")
    text.append(f"· {zone.name}  ", style="bold cyan")
    text.append(f"·  Lv.{state.level}  ", style="bold yellow")
    text.append(f"[{state.title}]", style="magenta")
    text.append(f"  🎯{zone.id}/∞" if zone.id >= 13 else f"  🎯{zone.id}/12", style="dim")
    if act:
        text.append(f"  [Acto {act.id}]", style=f"bold {act.color}")
    return Panel(text, border_style="bright_blue", box=box.HEAVY)


def render_zone_progress(completed: int, total: int, zone_name: str):
    """Barra de progreso de zona — se muestra al entrar."""
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    task = progress.add_task(f"[cyan]{zone_name}[/]", total=total)
    progress.update(task, completed=completed)
    console.print(progress)


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
    code_example: str | None = None,
    xp_reward: int = 0,
    hints_left: int = -1,
    act: Act | None = None,
):
    header = Text()
    header.append(f"  ▶ MISIÓN {mission_num}/{mission_total}", style="bold yellow")
    header.append(f"  ─  {title}", style="bold white")
    header.append(f"  (+{xp_reward} XP)", style="dim green")

    if act and act.max_hints_per_mission >= 0:
        header.append(f"  [💡{hints_left}/{act.max_hints_per_mission}]", style="dim cyan")

    console.print(Panel(header, border_style="yellow", box=box.SQUARE, padding=(0, 1)))
    console.print(Text(description, style="white"), highlight=True)

    if code_example:
        example_panel = Panel(
            Text(code_example, style="dim cyan"),
            title="Ejemplo",
            border_style="dim cyan",
            box=box.ROUNDED,
            padding=(0, 1),
            width=60,
        )
        console.print(example_panel)

    console.print()


def render_act_rules(act: Act):
    rules = []
    if act.max_hints_per_mission == -1:
        rules.append("💡 Pistas: ilimitadas")
    elif act.max_hints_per_mission == 0:
        rules.append("🚫 Sin pistas disponibles")
    else:
        rules.append(f"💡 Pistas: {act.max_hints_per_mission} por misión")
    rules.append("📝 Código base: " + ("siempre presente" if act.code_template_required else "opcional"))
    rules.append("⏭️ Saltar: " + ("permitido (-50 XP)" if act.allow_skip_with_penalty else "no permitido"))
    rules.append(f"⚡ XP: x{act.xp_multiplier} multiplicador")

    panel = Panel(
        Text("\n".join(f"  • {r}" for r in rules), style="dim"),
        title=f"Reglas del Acto {act.id}",
        border_style=act.color,
        box=box.SIMPLE,
    )
    console.print(panel)


def render_meta_moment(zone_id: int, mission_num: int):
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
                "[dim]      zone_range: tuple # (1,4), (5,9)...[/]\n"
                "[dim]      max_hints_per_mission: int[/]\n"
                "[dim]      xp_multiplier: float[/]\n\n"
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
                "[dim]  def validate_code(code, mode, test_cases):[/]\n"
                "[dim]      for tc in test_cases:[/]\n"
                "[dim]          result = execute_code(code, mode, tc.input)[/]\n"
                "[dim]          if result.stdout != tc.expected:[/]\n"
                "[dim]              return False[/]\n\n"
                "[italic]El templo es el código que lo ejecuta.[/]"
            ),
        },
    }
    if zone_id in momentos and mission_num in momentos[zone_id]:
        msg = momentos[zone_id][mission_num]
        console.print(Panel(Text.from_markup(msg), border_style="bold cyan", box=box.DOUBLE, padding=(1, 2)))
        console.input(Align.center(Text("[dim]Presiona Enter para asimilarlo...[/]")))


def render_zone_creator_intro():
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
        "Usa desde la terminal:\n"
        "  [green]python main.py --validate mi_zona.py[/]"
    )
    console.print(Panel(Text.from_markup(msg), border_style="yellow", box=box.HEAVY, padding=(1, 2)))
    console.input(Align.center(Text("[dim]Presiona Enter para comenzar...[/]")))


def render_execution_spinner(mode: str = "code") -> Live:
    """Crea un spinner contextual durante la ejecución de código."""
    texts = {
        "code": "Ejecutando tu código en el núcleo...",
        "zone": "Abriendo portal a la zona...",
        "validate": "Analizando tu arquitectura...",
    }
    spinner = Spinner("dots", text=texts.get(mode, "Procesando..."), style="cyan")
    return Live(spinner, refresh_per_second=10, transient=True)


def render_result(
    state: GameState,
    passed: bool,
    msg: str,
    xp: int = 0,
    old_level: int = 0,
):
    """Panel de resultado — éxito o fallo con formato rico."""
    if passed:
        console.print(Panel(
            Text(f"  ✔ {msg}  (+{xp} XP)", style="bold green"),
            border_style="green",
            box=box.HEAVY,
            padding=(0, 1),
        ))
        pct = state.xp_progress * 100
        bar = ProgressBar(total=state.xp_for_next, completed=state.xp, width=30)
        console.print(f"  [yellow]Lv.{state.level}[/] [cyan]{state.title}[/]  [dim]{state.xp}/{state.xp_for_next} ({pct:.0f}%)[/]")
        console.print(bar)

        if state.level > old_level:
            render_level_up(state, old_level)
    else:
        console.print(Panel(
            Text(f"  ✗ {msg}", style="bold red"),
            border_style="red",
            box=box.SQUARE,
            padding=(0, 1),
        ))


def render_level_up(state: GameState, old_level: int):
    """Evento de nivel — momento memorable con aparición progresiva."""
    time.sleep(0.3)
    lines = [
        ("", ""),
        (f"  ⚡ NIVEL {state.level} — {state.title.upper()}  ", f"bold yellow on {_level_color(state.level)}"),
        (f"  +{state.xp_for_next} XP hacia el siguiente nivel  ", "dim white"),
        ("", ""),
    ]
    for text, style in lines:
        panel = Panel(Text(text, style=style), border_style="yellow", box=box.DOUBLE, padding=(0, 2))
        console.print(Align.center(panel))
        time.sleep(0.15)


def _level_color(level: int) -> str:
    if level >= 20:
        return "bright_yellow"
    elif level >= 15:
        return "magenta"
    elif level >= 10:
        return "cyan"
    elif level >= 5:
        return "green"
    return "blue"


def render_zone_complete(
    zone_name: str,
    zone_id: int,
    total_missions: int,
    completed: int,
    skipped: int,
    failed: int,
    hints_used: int,
    xp_gained: int,
    time_spent: float,
):
    """Tabla de stats al final de zona."""
    mins, secs = divmod(int(time_spent), 60)

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", width=14)
    table.add_column(style="white")

    accuracy = (completed / max(1, completed + failed)) * 100

    table.add_row("  Tiempo", f"{mins} min {secs} seg")
    table.add_row("  Intentos", str(completed + failed))
    table.add_row("  Fallos", str(failed))
    table.add_row("  Pistas", str(hints_used))
    table.add_row("  XP ganado", str(xp_gained))
    table.add_row("  Precisión", f"{accuracy:.0f}%")

    console.print(Panel(
        Align.center(table),
        title=f"Zona {zone_id} completada — {zone_name}",
        border_style="green",
        box=box.HEAVY,
        padding=(1, 2),
    ))


def show_commands():
    table = Table(title="Comandos", box=box.SIMPLE, header_style="bold cyan")
    table.add_column("Comando", style="yellow")
    table.add_column("Acción", style="white")
    table.add_row("/perfil", "Ver tu perfil y medallas")
    table.add_row("/mapa", "Ver el mapa de zonas")
    table.add_row("/acto", "Ver las reglas del acto actual")
    table.add_row("/crear", "Generar template de zona (Zona ∞)")
    table.add_row("/validar <ruta>", "Validar una zona creada por ti")
    table.add_row("/ayuda", "Mostrar esta ayuda")
    table.add_row("/salir", "Guardar y salir")
    console.print(table)
