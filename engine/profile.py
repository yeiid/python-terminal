"""Perfil del jugador con tabs: Stats, Medallas, Battle Pass, Colección."""

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress_bar import ProgressBar
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align
from rich import box
from engine.state import GameState, ALL_ACHIEVEMENTS
from engine.acts import get_act, ACTS
from engine.battlepass import render_battle_pass
from engine.collection import render_collection
from engine.menu import render_tab_bar
from engine.console import console
from engine.curriculum import get_total_progress, get_topic_progress, STATUS_ICONS, STATUS_LABELS
from engine.pyhelp import TOPICS, CATEGORIES


PROFILE_TABS = [
    {"label": "Stats",      "icon": "📊"},
    {"label": "Medallas",   "icon": "🏅"},
    {"label": "Battle Pass","icon": "🏆"},
    {"label": "Colección",  "icon": "💠"},
    {"label": "Temas",      "icon": "📚"},
]


def show_profile(state: GameState):
    active_tab = 0
    while True:
        console.clear()
        title_text = Text()
        title_text.append("╔══════════════════════════════════════════╗\n", style="bold magenta")
        title_text.append(f"║     PERFIL DE {state.player_name.upper():<30} ║\n", style="bold yellow")
        title_text.append("╚══════════════════════════════════════════╝", style="bold magenta")
        console.print(Align.center(title_text))
        console.print()
        console.print(render_tab_bar(PROFILE_TABS, active_tab))
        console.print()

        if active_tab == 0:
            _render_stats_tab(state)
        elif active_tab == 1:
            _render_medals_tab(state)
        elif active_tab == 2:
            _render_battlepass_tab(state)
        elif active_tab == 3:
            _render_collection_tab(state)
        elif active_tab == 4:
            _render_topics_tab()

        console.print()
        console.print(Align.center(Text("[dim]← → Navegar tabs  |  Enter Volver[/]", style="dim italic")))
        key = _get_tab_key(active_tab, len(PROFILE_TABS))
        if key == "select":
            break
        elif key == "next":
            active_tab = (active_tab + 1) % len(PROFILE_TABS)
        elif key == "prev":
            active_tab = (active_tab - 1) % len(PROFILE_TABS)


def _get_tab_key(current: int, total: int) -> str:
    import sys
    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == "\t":
            return "next"
        if ch == "\x1b":
            ch2 = sys.stdin.read(2)
            if ch2 == "[D":
                return "prev"
            elif ch2 == "[C":
                return "next"
        if ch == "\r" or ch == "\n":
            return "select"
        if ch == "\x7f":
            return "select"
    except:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return "select"


def _render_xp_bar(state: GameState) -> Panel:
    pct = state.xp_progress * 100
    bar = ProgressBar(total=state.xp_for_next, completed=state.xp, width=40)
    content = Group(
        Text(f"  NIVEL {state.level}  [{state.title}]", style="bold yellow"),
        Text(f"XP: {state.xp}/{state.xp_for_next} ({pct:.0f}%)", style="dim"),
        bar,
    )
    return Panel(content, title="Progreso", border_style="green")


def _render_stats_tab(state: GameState):
    console.print(_render_xp_bar(state))
    console.print()

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column(style="white")

    act = get_act(state.unlocked_zones)
    missions_total = state.total_missions
    missions_pct = (missions_total / 60) * 100 if missions_total else 0
    total_time = state.total_play_time
    hours, rem = divmod(int(total_time), 3600)
    minutes, secs = divmod(rem, 60)
    time_str = f"{hours}h {minutes}m {secs}s" if hours else f"{minutes}m {secs}s"

    table.add_row("🎭  Acto actual:", f"{act.id} — {act.name}")
    table.add_row("🎯  Misiones completadas:", f"{missions_total}/60 ({missions_pct:.0f}%)")
    table.add_row("🗺️  Zonas desbloqueadas:", f"{state.unlocked_zones}/∞")
    table.add_row("📊  XP total ganado:", f"{state.total_xp_earned}")
    table.add_row("💡  Pistas usadas:", str(state.hints_used))
    table.add_row("⏭️  Saltadas:", str(state.missions_skipped))
    table.add_row("❌  Fallidas:", str(state.missions_failed))
    table.add_row("⏱️  Tiempo total:", time_str)
    table.add_row("🏅  Medallas:", f"{len(state.achievements)}/{len(ALL_ACHIEVEMENTS)}")
    table.add_row("📅  Primera sesión:", state.first_play_date)
    table.add_row("📅  Última sesión:", state.last_session_date)
    if state.player_zones_created:
        table.add_row("✨  Zonas creadas:", str(len(state.player_zones_created)))

    console.print(Panel(table, title="Estadísticas", border_style="cyan"))


def _render_medals_tab(state: GameState):
    medals = state.get_medals()
    unlocked = [m for m in medals if m["unlocked"]]
    locked = [m for m in medals if not m["unlocked"]]

    medal_texts = []
    for m in unlocked:
        t = Text()
        t.append(f"  {m['icon']} ", style="bold")
        t.append(m["name"], style="bold green")
        medal_texts.append(t)

    for m in locked:
        t = Text()
        t.append(f"  🔒 ", style="dim")
        t.append(m["name"], style="dim")
        medal_texts.append(t)

    if not medal_texts:
        medal_texts.append(Text("  (Aún no tienes medallas. ¡Sigue jugando!)", style="dim italic"))

    columns = Columns(medal_texts, equal=False, expand=True)
    console.print(Panel(
        Group(Text(f"  Desbloqueadas: {len(unlocked)}/{len(medals)}", style="cyan"), columns),
        title="Medallas y Logros",
        border_style="yellow",
    ))

    console.print()
    _render_acts_progress(state)


def _render_acts_progress(state: GameState):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold", width=6)
    table.add_column(style="white", width=22)
    table.add_column(style="white", width=12)
    current_act = get_act(state.unlocked_zones)

    for act in ACTS:
        start, end = act.zone_range
        if start > 12:
            continue
        completed = sum(1 for z in range(start, end + 1) if z in state.completed_zones)
        total_in_act = end - start + 1
        status = "▶" if act.id == current_act.id else "✓" if completed == total_in_act else "🔒"
        color = "yellow" if act.id == current_act.id else "green" if completed == total_in_act else "dim"
        style = f"bold {color}" if act.id == current_act.id else color
        table.add_row(
            f"[{style}]{act.id}[/]",
            f"[{style}]{act.name}[/]",
            f"[{style}]{'✓ Completo' if completed == total_in_act else f'{completed}/{total_in_act}'}[/]",
        )

    console.print(Panel(table, title="Progresión por Actos", border_style="blue"))


def _render_battlepass_tab(state: GameState):
    render_battle_pass(state.total_xp_earned)


def _render_collection_tab(state: GameState):
    render_collection(state.collected_objects or [])


def _render_topics_tab():
    completed, total, xp_total, pct = get_total_progress()
    bar = ProgressBar(total=total, completed=completed, width=30)

    console.print(Panel(
        Group(
            Text(f"  📚 Progreso de temas: {completed}/{total} ({pct}%)", style="bold cyan"),
            bar,
            Text(f"  XP total de temas: {xp_total}", style="green"),
        ),
        title="Aprendizaje",
        border_style="cyan",
    ))
    console.print()

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold", width=22)
    table.add_column(style="white", width=8)
    table.add_column(style="white", width=10)
    table.add_column(style="white", width=8)

    for cat_name in CATEGORIES:
        from engine.curriculum import get_category_progress
        c, t, x = get_category_progress(cat_name)
        p = f"{int((c/t)*100)}%" if t else "0%"
        table.add_row(f"  {cat_name}", f"{c}/{t}", p, f"+{x} XP")

    console.print(Panel(table, title="Por Categoría", border_style="blue"))

    console.print()
    console.print("[dim]Usa [cyan]/temas[/] para ver el panel completo de aprendizaje.[/]")
