import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from rich.console import Group


class TestProfile(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    def test_profile_tabs_defined(self):
        from engine.profile import PROFILE_TABS
        self.assertEqual(len(PROFILE_TABS), 5)
        labels = [t["label"] for t in PROFILE_TABS]
        self.assertIn("Stats", labels)
        self.assertIn("Medallas", labels)
        self.assertIn("Battle Pass", labels)
        self.assertIn("Colección", labels)
        self.assertIn("Temas", labels)

    def test_render_xp_bar(self):
        from engine.profile import _render_xp_bar
        from engine.state import GameState
        state = GameState()
        result = _render_xp_bar(state)
        self.assertIsInstance(result.renderable, Group)
        rendered = "".join(str(r) for r in result.renderable.renderables)
        self.assertIn("NIVEL", rendered)

    def test_render_stats_tab(self):
        from engine.profile import _render_stats_tab
        from engine.state import GameState
        state = GameState()
        with patch("engine.console.console.print"):
            _render_stats_tab(state)

    def test_render_medals_tab(self):
        from engine.profile import _render_medals_tab
        from engine.state import GameState
        state = GameState()
        with patch("engine.console.console.print"):
            _render_medals_tab(state)

    def test_render_battlepass_tab(self):
        from engine.profile import _render_battlepass_tab
        from engine.state import GameState
        state = GameState()
        with patch("engine.profile.render_battle_pass") as mock:
            with patch("engine.console.console.print"):
                _render_battlepass_tab(state)
                mock.assert_called_once()

    def test_render_collection_tab(self):
        from engine.profile import _render_collection_tab
        from engine.state import GameState
        state = GameState()
        with patch("engine.profile.render_collection") as mock:
            with patch("engine.console.console.print"):
                _render_collection_tab(state)
                mock.assert_called_once()

    def test_render_topics_tab(self):
        from engine.profile import _render_topics_tab
        with patch("engine.console.console.print"):
            _render_topics_tab()


if __name__ == "__main__":
    unittest.main()
