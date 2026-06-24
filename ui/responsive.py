import os
import sys


class ResponsiveConfig:
    def __init__(self):
        self._width = self._detect_width()
        self._is_termux = self._detect_termux()

    def _detect_termux(self) -> bool:
        return "TERMUX_VERSION" in os.environ

    def _detect_width(self) -> int:
        try:
            return os.get_terminal_size().columns
        except (ValueError, OSError):
            return 80

    @property
    def is_termux(self) -> bool:
        return self._is_termux

    @property
    def width(self) -> int:
        self._width = self._detect_width()
        return self._width

    @property
    def compact(self) -> bool:
        return self._is_termux or self._width < 80

    @property
    def max_content_width(self) -> int:
        if self._is_termux:
            return min(60, self._width - 4)
        if self._width < 80:
            return self._width - 4
        return 76

    @property
    def border_style(self) -> str:
        if self._is_termux:
            return "simple"
        if self._width < 80:
            return "simple"
        return "heavy"

    @property
    def progress_bar_width(self) -> int:
        if self._is_termux:
            return 15
        if self._width < 80:
            return 20
        return 30

    @property
    def indent(self) -> str:
        return "  " if self.compact else "    "

    @property
    def theme_name(self) -> str:
        if self._is_termux:
            return "termux"
        return "default"


responsive = ResponsiveConfig()
