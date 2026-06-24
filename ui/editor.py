from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from pygments.lexers import Python3Lexer

EDITOR_STYLE = Style.from_dict({
    "status": "bg:#222222 #ffffff",
})


def _build_toolbar(hints_left: int) -> FormattedText:
    items: list[tuple[str, str]] = [
        ("bg:#222222 fg:#ffffff", " "),
        ("bg:#222222 fg:#00ff87 bold", "Ctrl+D"),
        ("bg:#222222 fg:#ffffff", " enviar  |  "),
        ("bg:#222222 fg:#00ff87 bold", "Ctrl+C"),
        ("bg:#222222 fg:#ffffff", " cancelar  |  "),
        ("bg:#222222 fg:#888888", "Enter"),
        ("bg:#222222 fg:#ffffff", " nueva linea"),
    ]
    if hints_left >= 0:
        items += [
            ("bg:#222222 fg:#ffffff", "  |  "),
            ("bg:#222222 fg:#ffd700", f" {hints_left} hints"),
        ]
    items.append(("bg:#222222 fg:#ffffff", " "))
    return FormattedText(items)


def mini_editor(
    hints_left: int = -1,
    initial_text: str = "",
) -> str | None:
    bindings = KeyBindings()

    @bindings.add("c-d")
    def _(event):
        event.current_buffer.validate_and_handle()

    @bindings.add("c-c")
    def _cancel(event):
        event.app.exit(exception=KeyboardInterrupt)

    session = PromptSession(
        multiline=True,
        lexer=PygmentsLexer(Python3Lexer),
        key_bindings=bindings,
        history=InMemoryHistory(),
        style=EDITOR_STYLE,
        include_default_pygments_style=True,
        enable_history_search=False,
    )

    try:
        text = session.prompt(
            FormattedText([("fg:ansibrightgreen", ">>> ")]),
            bottom_toolbar=_build_toolbar(hints_left),
            default=initial_text,
        )
        return text.strip()
    except KeyboardInterrupt:
        return None
