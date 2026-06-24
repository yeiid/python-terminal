import os
import sys
import unittest


class TestIndentation(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    def test_format_code_output(self):
        from ui.indentation import format_code_output
        code = "print('hola')\nprint('mundo')"
        result = format_code_output(code, indent_level=1)
        lines = result.split("\n")
        for line in lines:
            self.assertTrue(line.startswith("  "))
        self.assertIn("print('hola')", result)

    def test_format_code_no_indent(self):
        from ui.indentation import format_code_output
        code = "x = 1"
        result = format_code_output(code, indent_level=0)
        self.assertEqual(result, "x = 1")

    def test_format_comparison_equal(self):
        from ui.indentation import format_comparison
        result = format_comparison("hola", "hola")
        self.assertIn("✓", result)

    def test_format_comparison_different(self):
        from ui.indentation import format_comparison
        result = format_comparison("hola", "mundo")
        self.assertIn("✗", result)
        self.assertIn("esperado", result)
        self.assertIn("recibido", result)

    def test_format_comparison_multiline(self):
        from ui.indentation import format_comparison
        result = format_comparison("a\nb\nc", "a\nx\nc")
        self.assertIn("✓", result)
        self.assertIn("✗", result)

    def test_show_expected_vs_received_runs(self):
        from ui.indentation import show_expected_vs_received
        try:
            show_expected_vs_received("expected", "received", case_num=1)
        except Exception as e:
            self.fail(f"show_expected_vs_received raised: {e}")


if __name__ == "__main__":
    unittest.main()
