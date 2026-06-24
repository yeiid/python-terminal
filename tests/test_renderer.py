"""Tests para engine/renderer.py — Funciones de renderizado."""

import unittest
from engine.renderer import (
    show_commands, make_header, render_zone_progress,
    render_story, render_mission, render_result,
    render_meta_moment, render_zone_creator_intro,
    render_execution_spinner, render_zone_complete,
    show_title_screen, IS_TERMUX, COMPACT,
    show_welcome_new_player, show_quick_tutorial,
    render_orientation_bar, show_return_dashboard,
    type_print, _level_color,
)
from ui.responsive import responsive
from engine.state import GameState
from engine.acts import get_act
from world.zones import Zone, Mission, TestCase


class TestResponsiveVars(unittest.TestCase):
    def test_is_termux_is_bool(self):
        self.assertIsInstance(IS_TERMUX, bool)

    def test_compact_is_bool(self):
        self.assertIsInstance(COMPACT, bool)

    def test_responsive_width(self):
        w = responsive.width
        self.assertIsInstance(w, int)
        self.assertGreater(w, 0)


class TestLevelColor(unittest.TestCase):
    def test_level_1_blue(self):
        self.assertEqual(_level_color(1), "blue")

    def test_level_5_green(self):
        self.assertEqual(_level_color(5), "green")

    def test_level_10_cyan(self):
        self.assertEqual(_level_color(10), "cyan")

    def test_level_15_magenta(self):
        self.assertEqual(_level_color(15), "magenta")

    def test_level_20_bright_yellow(self):
        self.assertEqual(_level_color(20), "bright_yellow")


class TestMakeHeader(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.zone = Zone(
            id=1, name="Test Zone",
            story_intro="Test",
        )

    def test_header_returns_panel(self):
        from rich.panel import Panel
        header = make_header(self.zone, self.state)
        self.assertIsInstance(header, Panel)

    def test_header_with_act(self):
        from rich.panel import Panel
        act = get_act(1)
        header = make_header(self.zone, self.state, act)
        self.assertIsInstance(header, Panel)


class TestShowCommands(unittest.TestCase):
    def test_show_commands_runs(self):
        try:
            show_commands()
        except Exception as e:
            self.fail(f"show_commands raised {e}")


class TestRenderZoneProgress(unittest.TestCase):
    def test_render_runs(self):
        try:
            render_zone_progress(0, 5, "Test Zone")
        except Exception as e:
            self.fail(f"render_zone_progress raised {e}")


class TestRenderStory(unittest.TestCase):
    def test_render_runs(self):
        try:
            render_story("Historia de prueba")
        except Exception as e:
            self.fail(f"render_story raised {e}")


class TestRenderMission(unittest.TestCase):
    def test_render_minimal(self):
        try:
            render_mission("Zone", 1, 5, "Mission 1", "Do something")
        except Exception as e:
            self.fail(f"render_mission raised {e}")

    def test_render_with_code_template(self):
        try:
            render_mission("Zone", 2, 5, "Mission 2", "Desc",
                           code_example="print('hello')", xp_reward=20)
        except Exception as e:
            self.fail(f"render_mission with template raised {e}")


class TestRenderResult(unittest.TestCase):
    def test_render_success(self):
        try:
            state = GameState()
            render_result(state, True, "OK", xp=50)
        except Exception as e:
            self.fail(f"render_result success raised {e}")

    def test_render_failure(self):
        try:
            state = GameState()
            render_result(state, False, "Error message")
        except Exception as e:
            self.fail(f"render_result failure raised {e}")

    def test_render_with_level_up(self):
        try:
            state = GameState(level=2)
            render_result(state, True, "OK", xp=150, old_level=1)
        except Exception as e:
            self.fail(f"render_result levelup raised {e}")


class TestRenderZoneComplete(unittest.TestCase):
    def test_render_runs(self):
        try:
            render_zone_complete(
                "Test Zone", 1, 5, 5, 0, 0, 2, 150, 120.5,
            )
        except Exception as e:
            self.fail(f"render_zone_complete raised {e}")


class TestRenderSpinner(unittest.TestCase):
    def test_spinner_various_modes(self):
        for mode in ["code", "zone", "validate", "pyhelp", "unknown"]:
            with self.subTest(mode=mode):
                spinner = render_execution_spinner(mode)
                self.assertIsNotNone(spinner)


class TestRenderMetaMoment(unittest.TestCase):
    def test_known_moment(self):
        try:
            from unittest.mock import patch
            with patch('builtins.input', return_value=''):
                render_meta_moment(6, 4)
        except Exception as e:
            self.fail(f"render_meta_moment (6,4) raised {e}")

    def test_unknown_moment(self):
        try:
            render_meta_moment(1, 1)
        except Exception as e:
            self.fail(f"render_meta_moment (1,1) raised {e}")


class TestRenderZoneCreator(unittest.TestCase):
    def test_render_runs(self):
        try:
            from unittest.mock import patch
            with patch('builtins.input', return_value=''):
                render_zone_creator_intro()
        except Exception as e:
            self.fail(f"render_zone_creator_intro raised {e}")


if __name__ == "__main__":
    unittest.main()
