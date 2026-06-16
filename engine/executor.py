import subprocess
import sys
import tempfile
from pathlib import Path


def execute_code(code: str, timeout: int = 5) -> tuple[str, str]:
    """Ejecuta código Python en un subproceso aislado.
    Retorna (stdout, stderr)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        script = Path(tmpdir) / "script.py"
        script.write_text(code)
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
            )
            return r.stdout.strip(), r.stderr.strip()
        except subprocess.TimeoutExpired:
            return "", "Timeout: el código tardó demasiado en ejecutarse"
        except Exception as e:
            return "", str(e)
