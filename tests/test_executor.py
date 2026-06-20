"""Tests para engine/executor.py — Ejecución aislada de código."""

import unittest
from engine.executor import (
    execute_code, _sanitize_code, _build_script, _clean_error,
    EXECUTION_TIMEOUT,
)
from world.zones import ExecutionResult


class TestSanitizeCode(unittest.TestCase):
    def test_safe_code_passes(self):
        code, err = _sanitize_code("print('hola')")
        self.assertIsNone(err)

    def test_block_eval(self):
        _, err = _sanitize_code("eval('1+1')")
        self.assertIsNotNone(err)
        self.assertIn("eval(", err)

    def test_block_exec(self):
        _, err = _sanitize_code("exec('x=1')")
        self.assertIsNotNone(err)

    def test_block_import(self):
        _, err = _sanitize_code("__import__('os')")
        self.assertIsNotNone(err)

    def test_block_os_system(self):
        _, err = _sanitize_code("os.system('ls')")
        self.assertIsNotNone(err)

    def test_block_os_popen(self):
        _, err = _sanitize_code("os.popen('ls')")
        self.assertIsNotNone(err)

    def test_block_subprocess(self):
        _, err = _sanitize_code("subprocess.run(['ls'])")
        self.assertIsNotNone(err)

    def test_block_compile(self):
        _, err = _sanitize_code("compile('1+1', '', 'eval')")
        self.assertIsNotNone(err)

    def test_allow_def(self):
        code, err = _sanitize_code("def foo(): pass")
        self.assertIsNone(err)

    def test_allow_print(self):
        code, err = _sanitize_code("print('hello')")
        self.assertIsNone(err)


class TestExecuteCodeScript(unittest.TestCase):
    def test_simple_print(self):
        r = execute_code("print('Hola')", mode="script")
        self.assertEqual(r.exit_code, 0)
        self.assertEqual(r.stdout, "Hola")

    def test_math_expression(self):
        r = execute_code("print(2 + 3)", mode="script")
        self.assertEqual(r.stdout, "5")

    def test_multiline_code(self):
        code = """x = 10
y = 20
print(x + y)"""
        r = execute_code(code, mode="script")
        self.assertEqual(r.stdout, "30")

    def test_empty_code(self):
        r = execute_code("", mode="script")
        self.assertEqual(r.exit_code, 1)
        self.assertIn("vacío", r.stderr)

    def test_whitespace_code(self):
        r = execute_code("   ", mode="script")
        self.assertEqual(r.exit_code, 1)
        self.assertIn("vacío", r.stderr)

    def test_syntax_error(self):
        r = execute_code("print('hola", mode="script")
        self.assertNotEqual(r.exit_code, 0)

    def test_blocked_eval_code(self):
        r = execute_code("eval('1+1')", mode="script")
        self.assertEqual(r.exit_code, 1)
        self.assertIn("no está disponible", r.stderr)

    def test_no_output(self):
        r = execute_code("x = 42", mode="script")
        self.assertEqual(r.exit_code, 0)
        self.assertEqual(r.stdout, "")


class TestExecuteCodeFunction(unittest.TestCase):
    def test_function_with_return(self):
        code = "def suma(a, b):\n    return a + b"
        r = execute_code(code, mode="function", test_input="[1, 2]")
        self.assertEqual(r.exit_code, 0, f"stderr: {r.stderr}")

    def test_function_no_args(self):
        code = "def hola():\n    return 'mundo'"
        r = execute_code(code, mode="function", test_input="")
        self.assertEqual(r.exit_code, 0, f"stderr: {r.stderr}")


class TestBuildScript(unittest.TestCase):
    def test_script_mode_passthrough(self):
        result = _build_script("print(1)", mode="script")
        self.assertEqual(result, "print(1)")

    def test_function_mode_wraps_code(self):
        result = _build_script("def foo(): return 42", mode="function")
        self.assertIn("def foo(): return 42", result)
        self.assertIn("_input", result)


class TestCleanError(unittest.TestCase):
    def test_traceback_cleaned(self):
        raw = """Traceback (most recent call last):
  File "script.py", line 1, in <module>
    print(1/0)
ZeroDivisionError: division by zero"""
        cleaned = _clean_error(raw)
        self.assertNotIn("Traceback", cleaned)
        self.assertIn("ZeroDivisionError", cleaned)

    def test_regular_error_passthrough(self):
        msg = "NameError: name 'x' is not defined"
        cleaned = _clean_error(msg)
        self.assertEqual(cleaned, msg)


class TestExecutionResult(unittest.TestCase):
    def test_result_dataclass(self):
        r = ExecutionResult(stdout="ok", stderr="", exit_code=0)
        self.assertEqual(r.stdout, "ok")
        self.assertFalse(r.timed_out)

    def test_timed_out_flag(self):
        r = ExecutionResult(stderr="timeout", timed_out=True, exit_code=-1)
        self.assertTrue(r.timed_out)


if __name__ == "__main__":
    unittest.main()
