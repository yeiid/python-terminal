"""Fixtures compartidos para todos los tests de PyQuest."""

import sys
import os
from pathlib import Path

# Asegurar que el directorio raíz está en sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Desactivar output de Rich durante tests
os.environ["TERM"] = "dumb"
os.environ["FORCE_COLOR"] = "0"
