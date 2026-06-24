from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress_bar import ProgressBar
from rich import box
from rich.align import Align
from rich.console import Group
from rich.progress import Progress, BarColumn, TextColumn

from rich.console import Console
from ui.responsive import responsive
from ui.themes import get_theme


console = Console(highlight=False)


def render_header(
    title: str,
    subtitle: str = "",
    level: int = 0,
    zone_id: int = 0,
    total_zones: int = 0,
    act_id: str = "",
    act_color: str = "green",
    border_style: str = "bright_blue",
) -> Panel:
    text = Text()
    text.append(f" {title} ", style=f"bold green")
    if subtitle:
        text.append(f"· {subtitle}  ", style="bold cyan")
    if level:
        text.append(f"·  Lv.{level}  ", style="bold yellow")
    if act_id:
        text.append(f"[{act_id}]", style=f"bold {act_color}")
    if zone_id:
        text.append(f"  {zone_id}/{total_zones if total_zones else '∞'}", style="dim")
    box_style = box.SIMPLE if responsive.compact else box.HEAVY
    return Panel(text, border_style=border_style, box=box_style)


def render_progress_bar(
    completed: int,
    total: int,
    label: str = "",
    width: int = 0,
) -> None:
    if width == 0:
        width = responsive.progress_bar_width
    pct = int((completed / total) * 100) if total else 0
    filled = int(width * completed / total) if total else 0
    bar = "█" * filled + "░" * (width - filled)
    if label:
        console.print(f"  {label} {bar} {completed}/{total} ({pct}%)")
    else:
        console.print(f"  {bar} {completed}/{total} ({pct}%)")


def render_rich_progress_bar(
    completed: int,
    total: int,
    zone_name: str = "",
) -> None:
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    if zone_name:
        task = progress.add_task(f"[cyan]{zone_name}[/]", total=total)
    else:
        task = progress.add_task(f"[cyan]Progreso[/]", total=total)
    progress.update(task, completed=completed)
    console.print(progress)


def render_panel(
    content: str | Text,
    title: str = "",
    border_style: str = "blue",
    box_type: str = "",
    padding: tuple[int, int] = (1, 2),
    width: int = 0,
) -> Panel:
    if not box_type:
        box_type = responsive.border_style
    box_map = {
        "heavy": box.HEAVY,
        "simple": box.SIMPLE,
        "rounded": box.ROUNDED,
        "square": box.SQUARE,
        "double": box.DOUBLE,
        "heavy_edge": box.HEAVY_EDGE,
    }
    b = box_map.get(box_type, box.HEAVY)
    if isinstance(content, str):
        content = Text(content)
    kw = dict(border_style=border_style, box=b, padding=padding)
    if width:
        kw["width"] = width
    elif responsive.max_content_width:
        kw["width"] = responsive.max_content_width
    return Panel(content, title=title, **kw)


def render_table(
    rows: list[list[str]],
    headers: list[str] | None = None,
    title: str = "",
    border_style: str = "blue",
    header_style: str = "bold cyan",
) -> Table:
    b = box.SIMPLE if responsive.compact else box.HEAVY_EDGE
    table = Table(
        box=b,
        show_header=bool(headers),
        header_style=header_style,
        border_style=border_style,
        title=title if not responsive.compact else "",
    )
    if headers:
        for h in headers:
            table.add_column(h)
    for row in rows:
        table.add_row(*row)
    return table


def render_orientation_bar(
    zone_id: int,
    zone_total: int,
    mission_num: int,
    mission_total: int,
    level: int,
    xp: int,
    hints_left: int = -1,
):
    hint_txt = "∞" if hints_left == -1 else str(hints_left)
    parts = [
        f"Z{zone_id}/{zone_total}",
        f"M{mission_num}/{mission_total}",
        f"Lv.{level}",
        f"{xp}XP",
        f"💡{hint_txt}",
    ]
    sep = " │ " if responsive.compact else "  │  "
    bar_text = sep.join(parts)
    bar_text += "  │  /ayuda"
    console.rule(f"[dim] {bar_text} [/]", style="dim bright_blue")
