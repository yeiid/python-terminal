import os
import sys
import unittest
from unittest.mock import patch, MagicMock


class TestMainFunctions(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    def test_handle_command_perfil(self):
        from main import handle_command
        from engine.state import GameState
        state = GameState()
        with patch("main.show_profile") as mock:
            result = handle_command("/perfil", state)
            self.assertTrue(result)
            mock.assert_called_once_with(state)

    def test_handle_command_mapa(self):
        from main import handle_command
        from engine.state import GameState
        state = GameState()
        with patch("main.show_map") as mock_map:
            with patch("builtins.input", return_value=""):
                result = handle_command("/mapa", state)
                self.assertTrue(result)
                mock_map.assert_called_once()

    def test_handle_command_acto(self):
        from main import handle_command
        from engine.state import GameState
        state = GameState()
        with patch("main.render_act_rules") as mock:
            with patch("builtins.input", return_value=""):
                result = handle_command("/acto", state)
                self.assertTrue(result)
                mock.assert_called_once()

    def test_handle_command_ayuda(self):
        from main import handle_command
        from engine.state import GameState
        state = GameState()
        with patch("main.show_help") as mock:
            result = handle_command("/ayuda", state)
            self.assertTrue(result)
            mock.assert_called_once()

    def test_handle_unknown(self):
        from main import handle_command
        from engine.state import GameState
        state = GameState()
        result = handle_command("/unknown", state)
        self.assertFalse(result)

    def test_get_multiline_input_code(self):
        from main import get_multiline_input
        from engine.state import GameState
        state = GameState()
        with patch("ui.editor.mini_editor", return_value="print('hola')"):
            result = get_multiline_input(state)
        self.assertEqual(result, "print('hola')")

    def test_get_multiline_input_cancel(self):
        from main import get_multiline_input
        from engine.state import GameState
        state = GameState()
        with patch("ui.editor.mini_editor", return_value=None):
            result = get_multiline_input(state)
        self.assertIsNone(result)

    def test_get_multiline_input_command(self):
        from main import get_multiline_input
        from engine.state import GameState
        state = GameState()
        with patch("ui.editor.mini_editor", return_value="/ayuda"):
            with patch("main.show_help"):
                result = get_multiline_input(state)
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
