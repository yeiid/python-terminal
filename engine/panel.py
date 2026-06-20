"""Panel de Temas — Navegador interactivo de aprendizaje PyQuest.

Uso desde el juego:
  /temas            → Abre el panel completo
  /temas <cat>      → Abre el panel en una categoría específica

Tabs: Fundamentos | Estructuras | Paradigmas | IO | Avanzado | Stats
"""

import sys
import termios
import tty
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.progress_bar import ProgressBar
from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.console import Group
from engine.console import console
from engine.pyhelp import TOPICS, CATEGORIES, get_topic, render_topic_detail
from engine.curriculum import (
    get_topic_progress, get_category_progress, get_total_progress,
    mark_practiced, mark_mastered, mark_viewed,
    STATUS_ICONS, STATUS_LABELS, STATUS_NEW, STATUS_LEARNING,
    STATUS_PRACTICED, STATUS_MASTERED,
)


PANEL_TABS = [
    {"label": "Fundamentos",   "icon": "📚"},
    {"label": "Estructuras",   "icon": "🗃️"},
    {"label": "Paradigmas",    "icon": "🏛️"},
    {"label": "IO",            "icon": "💾"},
    {"label": "Avanzado",      "icon": "⚡"},
    {"label": "Stats",         "icon": "📊"},
]

CATEGORY_TAB_MAP = {
    "Fundamentos": "Fundamentos",
    "Estructuras de Datos": "Estructuras",
    "Paradigmas": "Paradigmas",
    "IO": "IO",
    "Técnicas Avanzadas": "Avanzado",
    "Organización": "Avanzado",
    "Herramientas": "Avanzado",
}


def _get_key() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch2 = sys.stdin.read(2)
            if ch2 == "[A": return "up"
            if ch2 == "[B": return "down"
            if ch2 == "[C": return "right"
            if ch2 == "[D": return "left"
        if ch == "\t": return "tab"
        if ch == "\r" or ch == "\n": return "enter"
        if ch == "\x7f" or ch == "\x1b": return "back"
        if ch in ("p", "P"): return "practiced"
        if ch in ("d", "D"): return "mastered"
        return ch
    except:
        return "enter"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _get_categories_for_tab(tab_label: str) -> list[str]:
    if tab_label == "Stats":
        return []
    reverse_map = {}
    for cat, tab in CATEGORY_TAB_MAP.items():
        reverse_map.setdefault(tab, []).append(cat)
    return reverse_map.get(tab_label, [tab_label])


def _get_topics_for_tab(tab_label: str) -> list:
    if tab_label == "Stats":
        return []
    categories = _get_categories_for_tab(tab_label)
    result = []
    for cat in categories:
        result.extend(CATEGORIES.get(cat, []))
    return result


def _render_category_header(category: str):
    completed, total, xp = get_category_progress(category)
    pct = int((completed / total) * 100) if total else 0
    bar_width = 20
    filled = int(bar_width * pct / 100)
    bar = "█" * filled + "░" * (bar_width - filled)
    return f"  ▸ [bold cyan]{category}[/]  {bar} [green]{completed}/{total}[/] ([yellow]{pct}%[/])  XP: [green]+{xp}[/]"


def _render_topic_row(topic, selected: bool, idx: int) -> str:
    tp = get_topic_progress(topic.id)
    icon = STATUS_ICONS.get(tp.status, "📦")
    label = STATUS_LABELS.get(tp.status, "Nuevo")
    lvl_colors = {"Principiante": "green", "Intermedio": "yellow", "Avanzado": "red"}
    lvl_c = lvl_colors.get(topic.level, "white")

    selector = "▸" if selected else " "
    status_color = {
        STATUS_NEW: "dim",
        STATUS_LEARNING: "cyan",
        STATUS_PRACTICED: "green",
        STATUS_MASTERED: "yellow",
    }.get(tp.status, "dim")

    return (
        f"  {selector} {icon} [bold{' white' if selected else ''}]"
        f"{topic.id}[/]  —  {topic.title:<30}"
        f"  [{lvl_c}]({topic.level})[/]"
        f"  [{status_color}]{icon} {label}[/]"
        f"  [dim]+{tp.xp_earned} XP[/]"
    )


def _show_topic_detail(topic):
    """Muestra detalle del tema con opciones de progreso."""
    tp = get_topic_progress(topic.id)
    mark_viewed(topic.id)

    from engine.pyhelp import render_topic_detail as render_pyhelp_detail
    render_pyhelp_detail(topic.id)

    if tp.status not in (STATUS_MASTERED,):
        console.print()
        options = "[V]olver"
        if tp.status != STATUS_PRACTICED:
            options += "  [P]racticado (+20 XP)"
        if tp.status != STATUS_MASTERED:
            options += "  [D]ominado (+50 XP)"
        console.print(f"[yellow]{options}[/]")
        choice = _get_key()
        if choice == "practiced":
            gained = mark_practiced(topic.id)
            if gained:
                console.print(f"[green]✓ Marcado como Practicado. +{gained} XP[/]")
            else:
                console.print("[yellow]Ya estaba Practicado[/]")
            console.input("[dim]Presiona Enter para volver...[/]")
        elif choice == "mastered":
            gained = mark_mastered(topic.id)
            if gained:
                console.print(f"[green]✓ Marcado como Dominado. +{gained} XP[/]")
            else:
                console.print("[yellow]Ya estaba Dominado[/]")
            console.input("[dim]Presiona Enter para volver...[/]")


def _render_stats_panel():
    completed, total, xp_total, pct = get_total_progress()
    bar_width = 30
    filled = int(bar_width * pct / 100)
    bar = "█" * filled + "░" * (bar_width - filled)

    console.print(Text(f"\n  📊  PROGRESO GLOBAL", style="bold cyan"))
    console.print(f"  {bar}  [bold]{completed}/{total}[/] ([yellow]{pct}%[/])")
    console.print(f"  [green]XP total de temas: {xp_total}[/]")
    console.print()

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", width=20)
    table.add_column(style="white", width=14)
    table.add_column(style="white", width=10)
    table.add_column(style="white", width=10)

    for cat_name in CATEGORIES:
        completed_c, total_c, xp_c = get_category_progress(cat_name)
        pct_c = int((completed_c / total_c) * 100) if total_c else 0
        table.add_row(
            f"  {cat_name}",
            f"{completed_c}/{total_c}",
            f"{pct_c}%",
            f"+{xp_c} XP",
        )

    console.print(Panel(table, title="Progreso por Categoría", border_style="cyan"))
    console.print()

    status_counts = {STATUS_NEW: 0, STATUS_LEARNING: 0, STATUS_PRACTICED: 0, STATUS_MASTERED: 0}
    for t in TOPICS:
        tp = get_topic_progress(t.id)
        status_counts[tp.status] = status_counts.get(tp.status, 0) + 1

    counts_table = Table.grid(padding=(0, 3))
    counts_table.add_column(style="white", width=6)
    counts_table.add_column(style="white", width=16)
    for s, count in status_counts.items():
        icon = STATUS_ICONS.get(s, "📦")
        label = STATUS_LABELS.get(s, "Nuevo")
        counts_table.add_row(f"  {icon}", label, str(count))
    console.print(Panel(counts_table, title="Distribución de Estados", border_style="yellow"))
    console.print()

    if status_counts.get(STATUS_MASTERED, 0) == total:
        console.print("[bold yellow]🎉 ¡Has dominado todos los temas![/]")

    top_topic = None
    top_xp = -1
    for t in TOPICS:
        tp = get_topic_progress(t.id)
        if tp.xp_earned > top_xp:
            top_xp = tp.xp_earned
            top_topic = t
    if top_topic:
        console.print(f"[dim]📌 Tema más estudiado: {top_topic.icon} [cyan]{top_topic.title}[/] ({top_xp} XP)[/]")


def show_panel(filter_category: str = ""):
    """Muestra el panel interactivo de temas."""
    active_tab = 0
    if filter_category:
        for i, tab in enumerate(PANEL_TABS):
            if tab["label"].lower() == filter_category.lower():
                active_tab = i
                break

    while True:
        console.clear()
        title = Text("  📚  PANEL DE APRENDIZAJE  —  PyQuest", style="bold cyan")
        console.print(Align.center(title))
        console.print()

        # Tab bar
        tab_parts = []
        for i, tab in enumerate(PANEL_TABS):
            icon = tab["icon"]
            label = tab["label"]
            if i == active_tab:
                tab_parts.append(f"[bold white on blue] ▸ {icon} {label} [/]")
            else:
                tab_parts.append(f"[dim]{icon} {label}[/]")
        console.print(Panel(
            Text.from_markup("  " + "  ".join(tab_parts)),
            border_style="blue", box=box.SIMPLE, padding=(0, 0),
        ))
        console.print()

        current_tab = PANEL_TABS[active_tab]["label"]

        if current_tab == "Stats":
            _render_stats_panel()
        else:
            categories = _get_categories_for_tab(current_tab)
            topics = _get_topics_for_tab(current_tab)

            if not topics:
                console.print("[dim]No hay temas en esta categoría aún.[/]")
            else:
                selected_idx = 0
                while True:
                    # Render topics list
                    lines = []
                    seen_cats = set()
                    for topic in topics:
                        cat = topic.category
                        if cat not in seen_cats:
                            lines.append(("header", cat))
                            seen_cats.add(cat)
                        idx = topics.index(topic)
                        lines.append(("topic", topic, idx))

                    rendered_lines = []
                    for item in lines:
                        if item[0] == "header":
                            rendered_lines.append(_render_category_header(item[1]))
                            rendered_lines.append("")
                        else:
                            topic = item[1]
                            idx = item[2]
                            rendered_lines.append(_render_topic_row(topic, idx == selected_idx, idx))

                    for line in rendered_lines:
                        console.print(line)

                    console.print()
                    console.print("[dim]↑ ↓ Navegar  ·  Enter Ver detalle  ·  ← → Tabs  ·  Esc Volver[/]")

                    key = _get_key()

                    if key == "up" and selected_idx > 0:
                        selected_idx -= 1
                    elif key == "down" and selected_idx < len(topics) - 1:
                        selected_idx += 1
                    elif key == "left":
                        active_tab = (active_tab - 1) % len(PANEL_TABS)
                        break
                    elif key == "right":
                        active_tab = (active_tab + 1) % len(PANEL_TABS)
                        break
                    elif key in ("tab",):
                        active_tab = (active_tab + 1) % len(PANEL_TABS)
                        break
                    elif key == "enter":
                        if topics:
                            _show_topic_detail(topics[selected_idx])
                        break
                    elif key in ("back", "q", "Q"):
                        return
                    else:
                        break

        if current_tab != "Stats":
            if active_tab < 0:
                continue
        else:
            key = _get_key()
            if key == "left":
                active_tab = (active_tab - 1) % len(PANEL_TABS)
            elif key in ("right", "tab"):
                active_tab = (active_tab + 1) % len(PANEL_TABS)
            elif key in ("back", "q", "Q", "enter"):
                return
