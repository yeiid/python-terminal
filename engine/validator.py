"""Valida el código del jugador contra múltiples casos de prueba.

Cada caso de prueba se ejecuta en un subproceso aislado por separado,
usando el test_input correspondiente como entrada (stdin o argumento).
"""

from engine.executor import execute_code
from world.zones import TestCase
from ui.indentation import show_expected_vs_received


def validate_code(
    code: str,
    exec_mode: str,
    test_cases: list[TestCase],
    timeout: int = 5,
) -> tuple[bool, str, list[str]]:
    outputs: list[str] = []
    for i, tc in enumerate(test_cases, 1):
        result = execute_code(code, mode=exec_mode, test_input=tc.input, timeout=timeout)
        if result.timed_out:
            return False, f"Caso {i}: {result.stderr}", outputs
        if result.exit_code != 0:
            err = result.stderr.strip() or f"Error (código {result.exit_code})"
            return False, f"Caso {i}: {err}", outputs
        outputs.append(result.stdout)
        if tc.expected.strip() and result.stdout != tc.expected.strip():
            show_expected_vs_received(tc.expected, result.stdout, case_num=i)
            return (
                False,
                f"Caso {i} falló al evaluar con la entrada de prueba.",
                outputs,
            )
    total = len(test_cases)
    return True, f"✓ {total}/{total} casos pasaron.", outputs
