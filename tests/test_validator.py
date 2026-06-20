"""Tests para engine/validator.py — Validación de código del jugador."""

import unittest
from world.zones import TestCase
from engine.validator import validate_code


class TestValidateCode(unittest.TestCase):
    def test_simple_pass(self):
        passed, msg, outputs = validate_code(
            "print('Hola')",
            "script",
            [TestCase(input="", expected="Hola")],
        )
        self.assertTrue(passed)
        self.assertEqual(outputs, ["Hola"])

    def test_simple_fail(self):
        passed, msg, outputs = validate_code(
            "print('Chau')",
            "script",
            [TestCase(input="", expected="Hola")],
        )
        self.assertFalse(passed)
        self.assertIn("falló", msg)

    def test_multiple_cases_all_pass(self):
        passed, msg, outputs = validate_code(
            "print('ok')",
            "script",
            [TestCase(input="", expected="ok"), TestCase(input="", expected="ok")],
        )
        self.assertTrue(passed)
        self.assertEqual(len(outputs), 2)

    def test_multiple_cases_one_fails(self):
        passed, msg, outputs = validate_code(
            "print('ok')",
            "script",
            [TestCase(input="", expected="ok"), TestCase(input="", expected="fail")],
        )
        self.assertFalse(passed)

    def test_function_mode(self):
        passed, msg, outputs = validate_code(
            "def suma(a, b):\n    return a + b",
            "function",
            [TestCase(input="[1, 2]", expected="3")],
        )
        self.assertTrue(passed, f"msg: {msg}, outputs: {outputs}")

    def test_syntax_error_in_code(self):
        passed, msg, outputs = validate_code(
            "print('hola",
            "script",
            [TestCase(input="", expected="hola")],
        )
        self.assertFalse(passed)

    def test_dangerous_code_rejected(self):
        passed, msg, outputs = validate_code(
            "eval('1+1')",
            "script",
            [TestCase(input="", expected="2")],
        )
        self.assertFalse(passed)


if __name__ == "__main__":
    unittest.main()
