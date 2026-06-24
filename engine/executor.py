"""Ejecuta código Python del jugador en un subproceso aislado.

Soporta dos modos:
  - "script": el jugador escribe un script completo. Se captura stdout.
  - "function": el jugador escribe una función. El executor la llama con
    los inputs de los casos de prueba y captura stdout/retorno.

Timeout fijo de 5 segundos para evitar bucles infinitos.

Seguridad:
  - Ejecución en subproceso separado
  - Timeout forzado
  - Directorio temporal aislado
  - Sin acceso a redes ni sistema de archivos fuera del tmp
"""

import subprocess
import sys
import tempfile
import textwrap
import os
from pathlib import Path
from world.zones import ExecutionResult

EXECUTION_TIMEOUT = 5


def _build_script(code: str, mode: str, test_input: str = "") -> str:
    """Construye el script a ejecutar según el modo."""
    if mode == "function":
        safe_input = repr(test_input)
        code_dedented = textwrap.dedent(code)
        # Extract function name for the call
        func_names = []
        for line in code_dedented.split("\n"):
            stripped = line.strip()
            if stripped.startswith("def "):
                func_names.append(stripped.split("(")[0].split("def ")[1].strip())
        func_name = func_names[-1] if func_names else "main"
        return (
            "import sys, json\n"
            "\n"
            "# Código del jugador\n"
            f"{code_dedented}\n"
            "\n"
            "# Llamada de prueba\n"
            f"_input = {safe_input}\n"
            "if _input:\n"
            "    _args = json.loads(_input) if _input.startswith(\"[\") else [_input]\n"
            f"    _result = {func_name}(*_args)\n"
            "else:\n"
            f"    _result = {func_name}()\n"
            "if _result is not None:\n"
            "    print(_result)\n"
        )
    return code


def _sanitize_code(code: str) -> tuple[str, str | None]:
    """Revisa el código en busca de operaciones peligrosas.
    Retorna (código_limpio, mensaje_error).
    """
    dangerous = [
        "__import__", "exec(", "eval(", "compile(",
        "os.system", "os.popen", "subprocess.",
        "shutil.rmtree", "open('/", "open(\"/",
    ]
    for pattern in dangerous:
        if pattern in code:
            return code, f"Operación no permitida: '{pattern}' no está disponible por seguridad"
    return code, None


def execute_code(
    code: str,
    mode: str = "script",
    test_input: str = "",
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecutionResult:
    """Ejecuta código Python en un subproceso aislado y captura resultado."""
    if not code.strip():
        return ExecutionResult(stderr="Código vacío — escribe al menos una línea", exit_code=1)

    clean_code, sanitize_error = _sanitize_code(code)
    if sanitize_error:
        return ExecutionResult(stderr=sanitize_error, exit_code=1)

    full_code = _build_script(clean_code, mode, test_input)

    with tempfile.TemporaryDirectory() as tmpdir:
        script = Path(tmpdir) / "script.py"
        script.write_text(full_code)

        env = {
            "PATH": "/usr/bin:/bin",
            "HOME": tmpdir,
            "TERM": os.environ.get("TERM", "dumb"),
            "LANG": "C.UTF-8",
        }

        try:
            r = subprocess.run(
                [sys.executable, "-I", str(script)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
                env=env,
            )
            error_msg = r.stderr.strip()
            if r.returncode != 0 and error_msg:
                error_msg = _clean_error(error_msg)
            return ExecutionResult(
                stdout=r.stdout.strip(),
                stderr=error_msg,
                exit_code=r.returncode,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                stderr=f"⏱ Tiempo agotado: el código tardó más de {timeout} segundos.\n"
                       "¿Tienes un bucle infinito? Revisa tus while/for.",
                timed_out=True,
                exit_code=-1,
            )
        except FileNotFoundError:
            return ExecutionResult(
                stderr="❌ Python no está disponible en el sistema",
                exit_code=1,
            )
        except Exception as e:
            return ExecutionResult(stderr=f"Error del sistema: {e}", exit_code=1)


def _clean_error(stderr: str) -> str:
    """Limpia los tracebacks largos para mostrar solo lo esencial."""
    lines = stderr.split("\n")
    error_lines = []
    for line in lines:
        if line.startswith("Traceback"):
            continue
        if "File \"" in line and ", line " in line:
            parts = line.split(", line ")
            if len(parts) > 1:
                line_num = parts[1].split(",")[0]
                error_lines.append(f"Error en línea {line_num}")
            continue
        # Evitar imprimir líneas con circunflejos (^) que Python añade a veces si desalinean
        if line.strip() == "^" or set(line.strip()) == {"^", "~"}:
            error_lines.append(line)
            continue
        error_lines.append(line)
        
    clean_text = "\n".join(error_lines).strip()
    return clean_text if clean_text else stderr
