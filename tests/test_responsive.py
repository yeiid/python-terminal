import os
import sys
import unittest
from unittest.mock import patch


class TestResponsiveConfig(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    def test_default_not_termux(self):
        with patch.dict(os.environ, {}, clear=True):
            from ui.responsive import responsive
            self.assertFalse(responsive.is_termux)

    def test_termux_detected(self):
        with patch.dict(os.environ, {"TERMUX_VERSION": "0.118"}, clear=True):
            from ui.responsive import ResponsiveConfig
            rc = ResponsiveConfig()
            self.assertTrue(rc.is_termux)
            self.assertTrue(rc.compact)
            self.assertEqual(rc.theme_name, "termux")

    def test_compact_on_narrow(self):
        with patch.dict(os.environ, {}, clear=True):
            from ui.responsive import ResponsiveConfig
            rc = ResponsiveConfig()
            rc._width = 60
            self.assertTrue(rc.compact)
            self.assertEqual(rc.border_style, "simple")

    def test_max_content_width_termux(self):
        with patch.dict(os.environ, {"TERMUX_VERSION": "0.118"}, clear=True):
            from ui.responsive import ResponsiveConfig
            rc = ResponsiveConfig()
            rc._width = 80
            self.assertLessEqual(rc.max_content_width, 60)

    def test_indent_compact(self):
        with patch.dict(os.environ, {"TERMUX_VERSION": "0.118"}, clear=True):
            from ui.responsive import ResponsiveConfig
            rc = ResponsiveConfig()
            self.assertEqual(rc.indent, "  ")

    def test_indent_normal(self):
        with patch.dict(os.environ, {}, clear=True):
            from ui.responsive import ResponsiveConfig
            rc = ResponsiveConfig()
            rc._width = 120
            self.assertEqual(rc.indent, "    ")


class TestThemeSystem(unittest.TestCase):
    def test_default_theme(self):
        from ui.themes import get_theme
        theme = get_theme("default")
        self.assertEqual(theme.primary, "green")
        self.assertEqual(theme.error, "red")

    def test_termux_theme(self):
        from ui.themes import get_theme
        theme = get_theme("termux")
        self.assertTrue(theme.compact)
        self.assertEqual(theme.max_width, 60)

    def test_unknown_theme_falls_back(self):
        from ui.themes import get_theme
        theme = get_theme("nonexistent")
        self.assertEqual(theme.name, "default")


if __name__ == "__main__":
    unittest.main()
