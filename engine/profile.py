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
from engine.console import console


def render_xp_bar(state: GameState) -> Panel:
    pct = state.xp_progress * 100
    bar = ProgressBar(total=state.xp_for_next, completed=state.xp, width=40)
    content = Group(
        Text(f"  NIVEL {state.level}  [{state.title}]", style="bold yellow"),
        Text(f"XP: {state.xp}/{state.xp_for_next} ({pct:.0f}%)", style="dim"),
        bar,
    )
    return Panel(content, title="Progreso", border_style="green")


def render_stats(state: GameState) -> Panel:
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

    return Panel(table, title="Estadísticas", border_style="cyan")


def render_medals(state: GameState) -> Panel:
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
    return Panel(
        Group(Text(f"  Desbloqueadas: {len(unlocked)}/{len(medals)}", style="cyan"), columns),
        title="Medallas y Logros",
        border_style="yellow",
    )


def render_acts_progress(state: GameState) -> Panel:
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

    return Panel(table, title="Progresión por Actos", border_style="blue")


def render_zone_xp(state: GameState) -> Panel:
    if not state.xp_per_zone:
        return Panel(Text("Aún sin datos de XP por zona.", style="dim italic"), title="XP por Zona")

    table = Table.grid(padding=(0, 2))
    table.add_column(style="dim")
    table.add_column(style="white")
    table.add_column(style="yellow")
    for zid in sorted(state.xp_per_zone.keys(), key=int):
        xp = state.xp_per_zone[zid]
        nombre = f"Zona {zid}"
        table.add_row(f"  🎯 {nombre}", ":" , str(xp))
    return Panel(table, title="XP por Zona", border_style="green")


def show_profile(state: GameState):
    console.clear()
    title_text = Text()
    title_text.append("╔══════════════════════════════════════════╗\n", style="bold magenta")
    title_text.append(f"║     PERFIL DE {state.player_name.upper():<30} ║\n", style="bold yellow")
    title_text.append("╚══════════════════════════════════════════╝", style="bold magenta")
    console.print(Align.center(title_text))

    layout = Layout()
    layout.split_column(
        Layout(render_xp_bar(state)),
        Layout(render_stats(state)),
        Layout(render_acts_progress(state)),
        Layout(render_medals(state)),
    )
    console.print(layout)
    console.print(Align.center(Text("\nPresiona Enter para volver al juego...", style="dim italic")))
    input()
