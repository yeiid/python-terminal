#!/usr/bin/env python3
"""PyQuest Test Runner — Ejecuta todos los tests del proyecto.

Uso:
  python tests/run_all.py              # Todos los tests
  python tests/run_all.py -v           # Modo verbose
  python tests/run_all.py test_state   # Solo un módulo
  python tests/run_all.py -l           # Listar módulos disponibles
"""

import sys
import os
import unittest
import argparse
from pathlib import Path

# Asegurar que estamos en el directorio raíz
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ["TERM"] = "dumb"
os.environ["FORCE_COLOR"] = "0"


TEST_MODULES = [
    "test_executor",
    "test_validator",
    "test_schema",
    "test_state",
    "test_acts",
    "test_collection",
    "test_battlepass",
    "test_curriculum",
    "test_pyhelp",
    "test_discovery",
    "test_map",
    "test_renderer",
]


def list_modules():
    print("Módulos de test disponibles:")
    for m in TEST_MODULES:
        print(f"  - {m}")
    print(f"\nTotal: {len(TEST_MODULES)} módulos")


def run_tests(modules: list[str], verbosity: int = 1) -> int:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for mod_name in modules:
        try:
            mod = __import__(mod_name)
            tests = loader.loadTestsFromModule(mod)
            suite.addTests(tests)
            print(f"  ✓ {mod_name}")
        except ImportError as e:
            print(f"  ✗ {mod_name}: {e}")
            return 1
        except Exception as e:
            print(f"  ✗ {mod_name}: {e}")
            return 1

    print(f"\nEjecutando {len(modules)} módulo(s)...\n")

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    print(f"\n{'=' * 50}")
    print(f"Tests: {result.testsRun}  |  "
          f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}  |  "
          f"Failed: {len(result.failures)}  |  "
          f"Errors: {len(result.errors)}")
    print(f"{'=' * 50}")

    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description="PyQuest Test Runner")
    parser.add_argument("modules", nargs="*", help="Módulos a testear (default: todos)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbose output")
    parser.add_argument("-l", "--list", action="store_true", help="Listar módulos")
    args = parser.parse_args()

    if args.list:
        list_modules()
        return 0

    if args.modules:
        modules = [m if m.startswith("test_") else f"test_{m}" for m in args.modules]
        for m in modules:
            if m not in TEST_MODULES:
                print(f"Error: módulo '{m}' no encontrado")
                print(f"Usa -l para listar los módulos disponibles")
                return 1
    else:
        modules = TEST_MODULES

    verbosity = 1 + args.verbose
    return run_tests(modules, verbosity)


if __name__ == "__main__":
    sys.exit(main())
