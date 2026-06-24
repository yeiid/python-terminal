import os
import sys
import unittest
from unittest.mock import patch


class TestPanel(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    def test_panel_tabs_defined(self):
        from engine.panel import PANEL_TABS
        self.assertEqual(len(PANEL_TABS), 6)
        labels = [t["label"] for t in PANEL_TABS]
        self.assertIn("Fundamentos", labels)
        self.assertIn("Estructuras", labels)
        self.assertIn("Paradigmas", labels)
        self.assertIn("IO", labels)
        self.assertIn("Avanzado", labels)
        self.assertIn("Stats", labels)

    def test_get_categories_for_tab(self):
        from engine.panel import _get_categories_for_tab
        cats = _get_categories_for_tab("Fundamentos")
        self.assertIn("Fundamentos", cats)

    def test_get_categories_for_stats(self):
        from engine.panel import _get_categories_for_tab
        cats = _get_categories_for_tab("Stats")
        self.assertEqual(cats, [])

    def test_get_topics_for_tab(self):
        from engine.panel import _get_topics_for_tab
        topics = _get_topics_for_tab("Fundamentos")
        self.assertTrue(len(topics) > 0)

    def test_get_topics_for_stats(self):
        from engine.panel import _get_topics_for_tab
        topics = _get_topics_for_tab("Stats")
        self.assertEqual(topics, [])

    def test_render_stats_panel(self):
        from engine.panel import _render_stats_panel
        with patch("engine.console.console.print"):
            _render_stats_panel()


if __name__ == "__main__":
    unittest.main()
