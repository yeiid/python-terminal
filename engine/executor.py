"""Ejecuta código Python del jugador en un subproceso aislado.

Soporta dos modos:
  - "script": el jugador escribe un script completo. Se captura stdout.
  - "function": el jugador escribe una función. El executor la llama con
    los inputs de los casos de prueba y captura stdout/retorno.

Timeout fijo de 5 segundos para evitar bucles infinitos.
"""

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from world.zones import ExecutionResult

EXECUTION_TIMEOUT = 5  # segundos


def _build_script(code: str, mode: str, test_input: str = "") -> str:
    """Construye el script a ejecutar según el modo."""
    if mode == "function":
        # El jugador escribe una función. La envolvemos con llamadas.
        safe_input = repr(test_input)
        return textwrap.dedent(f"""\
        import sys, json

        # Código del jugador
        {code}

        # Llamada de prueba
        _input = {safe_input}
        if _input:
            _args = json.loads(_input) if _input.startswith("[") else [_input]
            _result = {code.split("def ")[1].split("(")[0] if "def " in code else "main"}(*_args)
        else:
            _result = {code.split("def ")[1].split("(")[0] if "def " in code else "main"}()
        if _result is not None:
            print(_result)
        """)
    # Modo script: ejecutar tal cual
    return code


def execute_code(
    code: str,
    mode: str = "script",
    test_input: str = "",
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecutionResult:
    """Ejecuta código Python en un subproceso aislado y captura resultado."""
    if not code.strip():
        return ExecutionResult(stderr="Código vacío", exit_code=1)

    full_code = _build_script(code, mode, test_input)

    with tempfile.TemporaryDirectory() as tmpdir:
        script = Path(tmpdir) / "script.py"
        script.write_text(full_code)
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
            )
            return ExecutionResult(
                stdout=r.stdout.strip(),
                stderr=r.stderr.strip(),
                exit_code=r.returncode,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                stderr=f"Timeout: el código tardó más de {timeout}s",
                timed_out=True,
                exit_code=-1,
            )
        except Exception as e:
            return ExecutionResult(stderr=str(e), exit_code=1)
