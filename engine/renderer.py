import time
import os
import sys
from pathlib import Path
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


def detect_termux() -> bool:
    return "TERMUX_VERSION" in os.environ


def detect_screen_width() -> int:
    try:
        return os.get_terminal_size().columns
    except:
        return 80


IS_TERMUX = detect_termux()
SCREEN_WIDTH = detect_screen_width()
COMPACT = IS_TERMUX or SCREEN_WIDTH < 80


def type_print(text: str, delay: float = 0.015, style: str = ""):
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(delay)
    console.print()


def get_ascii_logo() -> str:
    path = Path(__file__).resolve().parent.parent / "assets" / "ascii" / "logo.txt"
    if path.exists():
        return path.read_text()
    return ""


def show_title_screen(state: GameState):
    console.clear()
    logo = get_ascii_logo()
    if logo:
        console.print(Align.center(Text(logo, style="bold green")))
    elif COMPACT:
        console.print(Align.center(Text("  pyquest — terminal RPG\\n  aprende python como un héroe\\n", style="bold green")))
    else:
        t = Text()
        t.append("╔══════════════════════════════════════════╗\\n", style="bold green")
        t.append("║        ", style="bold green")
        t.append("pyquest", style="bold yellow")
        t.append(" — terminal RPG            ", style="bold green")
        t.append("║\\n", style="bold green")
        t.append("║   ", style="bold green")
        t.append("aprende python como un héroe", style="cyan")
        t.append("     ", style="bold green")
        t.append("║\\n", style="bold green")
        t.append("╚══════════════════════════════════════════╝", style="bold green")
        console.print(Align.center(t))

    if IS_TERMUX:
        console.print("[dim]📱 Modo Termux detectado — interfaz adaptada[/]")

    if not state.player_name or state.player_name == "Dev":
        state.player_name = console.input("[bold]\\n¿Cuál es tu nombre, dev? [/]")


def show_welcome_new_player():
    """Pantalla de onboarding para la primera vez — explica qué es PyQuest antes de empezar."""
    console.clear()
    welcome_text = Text()
    welcome_text.append("  ¡Bienvenido a PyQuest!\\n\\n", style="bold yellow")
    welcome_text.append("  PyQuest es un RPG de terminal donde aprendes Python\\n", style="white")
    welcome_text.append("  resolviendo misiones reales de código.\\n\\n", style="white")
    welcome_text.append("  ⚔️  Cómo funciona:\\n", style="bold cyan")
    welcome_text.append("    • Cada Zona cubre un tema de Python (~10 min)\\n", style="white")
    welcome_text.append("    • Cada Zona tiene 5 misiones que debes superar\\n", style="white")
    welcome_text.append("    • Escribes código → el juego lo evalúa → ganas XP\\n", style="white")
    welcome_text.append("    • Hay 12+ Zonas, desde variables hasta async/await\\n\\n", style="white")
    welcome_text.append("  🗺️  Ruta de aprendizaje:\\n", style="bold green")
    welcome_text.append("    Acto I   (Zonas 1-4)  → Fundamentos con guía completa\\n", style="green")
    welcome_text.append("    Acto II  (Zonas 5-9)  → Desarrollo con menos ayuda\\n", style="cyan")
    welcome_text.append("    Acto III (Zonas 10-12) → Arquitectura sin pistas\\n", style="magenta")
    welcome_text.append("    Acto ∞  (Zona 13+)    → Creas tus propias zonas\\n\\n", style="yellow")
    welcome_text.append("  💡 Comandos siempre disponibles:\\n", style="bold")
    welcome_text.append("    /ayuda → ver todos los comandos\\n", style="dim")
    welcome_text.append("    /mapa  → ver tu progreso\\n", style="dim")
    welcome_text.append("    /salir → guardar y cerrar\\n", style="dim")

    console.print(Panel(
        welcome_text,
        title="[bold yellow]📜 Bienvenida al mundo[/]",
        border_style="yellow",
        box=box.HEAVY,
        padding=(1, 2),
    ))
    console.input("[dim]Presiona Enter para comenzar el tutorial...[/]")


def show_quick_tutorial():
    """Tutorial interactivo de 2 pasos antes de la primera misión."""
    console.clear()

    # — Paso 1: Enviar código
    step1 = Text()
    step1.append("📖 Paso 1 de 2 — Cómo enviar código\\n\\n", style="bold cyan")
    step1.append("  Cuando veas el prompt  >>> escribe tu código Python.\\n", style="white")
    step1.append("  Para enviar (ejecutar) tu código:\\n\\n", style="white")
    if IS_TERMUX:
        step1.append("    En Termux: escribe una línea y presiona Enter\\n", style="yellow")
        step1.append("    Para código de múltiples líneas: usa Ctrl+D al final\\n", style="yellow")
    else:
        step1.append("    Una sola línea: presiona Enter\\n", style="yellow")
        step1.append("    Múltiples líneas: Ctrl+D al terminar de escribir\\n", style="yellow")
    step1.append("\\n  Ejemplo rápido — escribe esto cuando veas el prompt:\\n", style="white")
    step1.append("    print(\"Hola PyQuest\")\\n", style="bold green")

    console.print(Panel(
        step1,
        title="[bold cyan]🎮 Tutorial Rápido[/]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    console.input("[dim]Entendido — presiona Enter...[/]")
    console.clear()

    # — Paso 2: Pedir ayuda
    step2 = Text()
    step2.append("📖 Paso 2 de 2 — Cómo pedir ayuda\\n\\n", style="bold cyan")
    step2.append("  Si te atascas en una misión, tienes 4 recursos:\\n\\n", style="white")
    step2.append("  [H]  Pista     ", style="bold yellow")
    step2.append("→ una ayuda directa sin spoilers\\n", style="white")
    step2.append("  /docs        ", style="bold blue")
    step2.append("→ documentación interactiva de Python\\n", style="white")
    step2.append("  /playground  ", style="bold green")
    step2.append("→ REPL libre para experimentar\\n", style="white")
    step2.append("  [S]  Saltar   ", style="bold dim")
    step2.append("→ avanzar (cuesta 50 XP)\\n\\n", style="white")
    step2.append("  Recuerda: en cualquier momento escribe [bold]/ayuda[/] para ver todo.\\n", style="dim")
    step2.append("  Para salir de forma segura: [bold]/salir[/] (guarda tu progreso).\\n", style="dim")

    console.print(Panel(
        step2,
        title="[bold cyan]🆘 Recursos de Ayuda[/]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    console.input("[dim]¡Listo! Presiona Enter para comenzar tu primera misión...[/]")


def render_orientation_bar(
    zone_id: int,
    zone_total: int,
    mission_num: int,
    mission_total: int,
    state: "GameState",
    hints_left: int = -1,
):
    """Barra de contexto persistente encima de cada misión."""
    hint_txt = "💡 ∞" if hints_left == -1 else f"💡 {hints_left}"
    zone_info = f"Zona {zone_id}/{zone_total}"
    mission_info = f"Misión {mission_num}/{mission_total}"
    player_info = f"Lv.{state.level} · {state.xp} XP"
    console.rule(
        f"[dim] {zone_info}  │  {mission_info}  │  {player_info}  │  {hint_txt}  │  /ayuda [/]",
        style="dim bright_blue",
    )


DAILY_TIPS = [
    "💡 Usa [bold]/playground[/] para experimentar con Python libremente sin perder XP",
    "💡 [bold]/docs lista[/] abre la referencia de listas en Python",
    "💡 Si te atascas, [bold]/ayuda[/] muestra todos los comandos disponibles",
    "💡 Cada zona tiene un objeto coleccionable oculto — ¡búscalos en tu perfil!",
    "💡 [bold]/temas[/] muestra tu progreso de aprendizaje por categorías",
    "💡 Puedes crear tus propias zonas con [bold]/crear[/] cuando alcances la Zona 13",
    "💡 El Acto I tiene pistas ilimitadas — úsalas sin miedo",
    "💡 Escribe [bold]/mapa[/] para visualizar tu progreso en el mapa de zonas",
]


def show_daily_tip():
    """Muestra un tip rotativo al iniciar sesión."""
    import hashlib
    import time as _time
    # Rota el tip según el día actual (cambia cada día)
    day_key = int(_time.strftime("%j"))  # día del año (1-365)
    tip = DAILY_TIPS[day_key % len(DAILY_TIPS)]
    console.print(Panel(
        Text.from_markup(f"  {tip}"),
        title="[dim]💬 Tip del día[/]",
        border_style="dim",
        box=box.SIMPLE,
        padding=(0, 1),
    ))


def make_header(zone: "Zone", state: GameState, act: Act | None = None) -> Panel:
    text = Text()
    text.append(" ⚔️  PyQuest ", style="bold green")
    text.append(f"· {zone.name}  ", style="bold cyan")
    text.append(f"·  Lv.{state.level}  ", style="bold yellow")
    title_short = state.title[:5]
    text.append(f"[{title_short}]", style="magenta")
    text.append(f"  {zone.id}/∞" if zone.id >= 13 else f"  {zone.id}/12", style="dim")
    if act:
        text.append(f"  [{act.id}]", style=f"bold {act.color}")
    return Panel(text, border_style="bright_blue", box=box.HEAVY)


def render_zone_progress(completed: int, total: int, zone_name: str):
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
        max_w = min(60, SCREEN_WIDTH - 4) if COMPACT else 60
        example_panel = Panel(
            Text(code_example, style="dim cyan"),
            title="Ejemplo",
            border_style="dim cyan",
            box=box.ROUNDED,
            padding=(0, 1),
            width=max_w,
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


def show_return_dashboard(state: "GameState") -> str:
    """Dashboard de retorno para sesiones posteriores. Retorna la elección del usuario."""
    import datetime
    console.clear()

    # ── TIP DEL DÍA ──
    show_daily_tip()
    console.print()

    # Calcular progreso de zona actual
    total_completed = len(state.completed_missions)
    # Estimar misiones de zona actual completadas (5 por zona)
    zone_missions_done = len([m for m in state.completed_missions
                              if m.startswith(f"{state.unlocked_zones}-")])
    zone_total = 5  # constante por zona
    pct = int((zone_missions_done / zone_total) * 100)

    # Barra de progreso visual
    bar_len = 20
    filled = int(bar_len * zone_missions_done / zone_total)
    bar = "█" * filled + "░" * (bar_len - filled)

    # Tiempo desde última sesión
    try:
        last = datetime.datetime.strptime(state.last_session_date, "%Y-%m-%d %H:%M")
        diff = datetime.datetime.now() - last
        days = diff.days
        hours = diff.seconds // 3600
        if days > 0:
            time_ago = f"hace {days} día{'s' if days > 1 else ''}"
        elif hours > 0:
            time_ago = f"hace {hours} hora{'s' if hours > 1 else ''}"
        else:
            time_ago = "hace unos minutos"
    except Exception:
        time_ago = "sesión anterior"

    # XP progress
    xp_bar_len = 15
    xp_filled = int(xp_bar_len * state.xp_progress)
    xp_bar = "▪" * xp_filled + "·" * (xp_bar_len - xp_filled)

    dashboard = Text()
    dashboard.append(f"  👋 ¡Bienvenido de vuelta, {state.player_name}!\n", style="bold yellow")
    dashboard.append(f"  ⏰ Última sesión: {time_ago}\n\n", style="dim")
    dashboard.append(f"  ⚔️  Nivel {state.level}  ", style="bold green")
    dashboard.append(f"[{state.title}]", style="magenta")
    dashboard.append(f"  ·  {xp_bar}  {state.xp}/{state.xp_for_next} XP\n\n", style="dim")
    dashboard.append(f"  📍 Zona actual: ", style="bold")
    dashboard.append(f"Zona {state.unlocked_zones}\n", style="bold cyan")
    dashboard.append(f"  Progreso: {zone_missions_done}/{zone_total} misiones  ", style="white")
    dashboard.append(f"[{bar}] {pct}%\n\n", style="cyan")
    dashboard.append(f"  📊 Total completado: {total_completed} misiones  ", style="dim")
    dashboard.append(f"·  {len(state.achievements)} logros\n", style="dim")

    console.print(Panel(
        dashboard,
        title="[bold green]⚔️  PyQuest — Panel de Retorno[/]",
        border_style="bright_blue",
        box=box.HEAVY,
        padding=(1, 1),
    ))

    options = Text()
    options.append("  ¿Qué deseas hacer?\n\n", style="bold")
    options.append("  [C] ", style="bold green")  ; options.append("Continuar donde lo dejé\n", style="white")
    options.append("  [M] ", style="bold cyan")   ; options.append("Ver mapa de zonas\n", style="white")
    options.append("  [P] ", style="bold magenta") ; options.append("Ver mi perfil y logros\n", style="white")
    options.append("  [D] ", style="bold blue")   ; options.append("Ir a documentación Python\n", style="white")
    options.append("  [S] ", style="bold dim")    ; options.append("Guardar y salir\n", style="dim")
    console.print(options)

    while True:
        choice = console.input("[bold green]Tu elección (C/M/P/D/S): [/]").strip().lower()
        if choice in ("c", "m", "p", "d", "s", ""):
            return choice if choice else "c"
        console.print("[dim red]Opción no válida. Escribe C, M, P, D o S.[/]")


def render_meta_moment(zone_id: int, mission_num: int):
    momentos = {
        6: {
            4: (
                "[bold cyan]╔══════════════════════════════════════════╗\\n"
                "║  ENCONTRASTE LOS PLANOS DE LA CIUDAD      ║\\n"
                "╚══════════════════════════════════════════╝[/]\\n\\n"
                "Revisas los archivos del sistema y encuentras esto:\\n\\n"
                "[dim]  # engine/acts.py[/]\\n"
                "[dim]  class Act:[/]\\n"
                "[dim]      id: str           # I, II, III, ∞[/]\\n"
                "[dim]      name: str         # El Aprendiz...[/]\\n"
                "[dim]      zone_range: tuple # (1,4), (5,9)...[/]\\n"
                "[dim]      max_hints_per_mission: int[/]\\n"
                "[dim]      xp_multiplier: float[/]\\n\\n"
                "[italic]Alguien construyó esto antes que tú.[/]"
            ),
        },
        8: {
            3: (
                "[bold cyan]╔══════════════════════════════════════════╗\\n"
                "║  EL CÓDIGO SE MIRA A SÍ MISMO            ║\\n"
                "╚══════════════════════════════════════════╝[/]\\n\\n"
                "Los decoradores que estás aprendiendo...\\n"
                "son los mismos que usa el engine para validar tus misiones:\\n\\n"
                "[dim]  # engine/validator.py[/]\\n"
                "[dim]  def validate_code(code, mode, test_cases):[/]\\n"
                "[dim]      for tc in test_cases:[/]\\n"
                "[dim]          result = execute_code(code, mode, tc.input)[/]\\n"
                "[dim]          if result.stdout != tc.expected:[/]\\n"
                "[dim]              return False[/]\\n\\n"
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
    texts = {
        "code": "Ejecutando tu código en el núcleo...",
        "zone": "Abriendo portal a la zona...",
        "validate": "Analizando tu arquitectura...",
        "pyhelp": "Cargando documentación...",
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
    if passed:
        console.print(Panel(
            Text(f"  ✔ {msg}  (+{xp} XP)", style="bold green"),
            border_style="green",
            box=box.HEAVY,
            padding=(0, 1),
        ))
        bar_width = min(30, SCREEN_WIDTH - 20) if COMPACT else 30
        pct = state.xp_progress * 100
        bar = ProgressBar(total=state.xp_for_next, completed=state.xp, width=bar_width)
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
    table = Table(title="Comandos PyQuest", box=box.SIMPLE, header_style="bold cyan")
    table.add_column("Comando", style="yellow")
    table.add_column("Acción", style="white")
    table.add_row("/perfil", "Ver tu perfil completo (tabs)")
    table.add_row("/mapa", "Ver el mapa de zonas")
    table.add_row("/acto", "Ver las reglas del acto actual")
    table.add_row("/docs", "📚 Documentación interactiva de Python")
    table.add_row("/docs <tema>", "Ver un tema específico")
    table.add_row("/temas", "📚 Panel de aprendizaje con progreso")
    table.add_row("/playground", "🐍 REPL libre para experimentar")
    table.add_row("/crear", "Generar template de zona")
    table.add_row("/validar <ruta>", "Validar una zona creada por ti")
    table.add_row("/git pull", "Actualizar zonas desde Git")
    table.add_row("/ayuda", "Mostrar esta ayuda")
    table.add_row("/salir", "Guardar y salir")
    console.print(table)
