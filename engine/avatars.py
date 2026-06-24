from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box

def get_pixel_mentor() -> Text:
    """Retorna un personaje tipo pixel-art (Mago/Mentor)."""
    # Usaremos bloques unicode para simular píxeles de 8-bits
    art = (
        "      [magenta]▄▄▄▄▄[/]\n"
        "     [magenta]███████[/]\n"
        "    [magenta]█████████[/]\n"
        "   [magenta]███[/][white]▄▄▄▄▄[/][magenta]███[/]\n"
        "   [magenta]██[/][white]███████[/][magenta]██[/]\n"
        "   [magenta]██[/][white]█[/][cyan]▀[/][white]███[/][cyan]▀[/][white]█[/][magenta]██[/]\n"
        "    [white]█████████[/]\n"
        "     [white]███████[/]\n"
        "    [blue]▄███████▄[/]\n"
        "   [blue]███████████[/]\n"
        "  [blue]█████████████[/]\n"
    )
    return Text.from_markup(art)

def mentor_speaks(message: str, title: str = "Mentor PyQuest") -> Columns:
    """Retorna un layout con el mentor hablando y un bocadillo de texto."""
    avatar = get_pixel_mentor()
    msg_panel = Panel(
        Text.from_markup(message),
        title=f"[bold cyan]{title}[/]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    return Columns([avatar, msg_panel], padding=(0, 2))
