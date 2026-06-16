"""Validador de esquemas para zonas de PyQuest.

Valida zonas creadas por jugadores (Zona ∞) contra el schema
del engine (world/zones/__init__.py). También genera templates.
"""

import importlib.util
import sys
from pathlib import Path
from world.zones import Zone, Mission, TestCase

REQUIRED_ZONE_FIELDS = {"id", "name", "story_intro", "missions"}
REQUIRED_MISSION_FIELDS = {"num", "title", "description"}
MAX_MISSIONS_PER_ZONE = 10
BUILTIN_ZONE_MAX_ID = 12


def validate_zone_file(filepath: str | Path) -> list[str]:
    """Valida un archivo de zona. Retorna lista de errores (vacía = válido)."""
    errors = []
    filepath = Path(filepath)

    if not filepath.exists():
        return [f"Archivo no encontrado: {filepath}"]
    if filepath.suffix != ".py":
        return [f"Debe ser .py, no {filepath.suffix}"]

    spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
    if spec is None or spec.loader is None:
        return [f"No se pudo cargar {filepath}"]

    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return [f"Error de importación: {e}"]

    if not hasattr(mod, "zone"):
        return ["El archivo debe exportar `zone`"]

    zone = mod.zone
    if not isinstance(zone, Zone):
        return ["`zone` debe ser una instancia de la dataclass Zone (world/zones/)"]

    for field in REQUIRED_ZONE_FIELDS:
        if getattr(zone, field, None) is None:
            errors.append(f"Zone.{field}: campo requerido")

    if hasattr(zone, "id") and zone.id is not None:
        if zone.id <= BUILTIN_ZONE_MAX_ID:
            errors.append(
                f"Zone.id debe ser > {BUILTIN_ZONE_MAX_ID} "
                f"(las zonas 1-{BUILTIN_ZONE_MAX_ID} son del juego base). "
                f"ID actual: {zone.id}"
            )

    if not zone.missions:
        errors.append("La zona debe tener al menos 1 misión")
    else:
        if len(zone.missions) > MAX_MISSIONS_PER_ZONE:
            errors.append(f"Máximo {MAX_MISSIONS_PER_ZONE} misiones por zona")

        nums = [m.num for m in zone.missions]
        if len(nums) != len(set(nums)):
            errors.append("Los números de misión deben ser únicos")

        for i, m in enumerate(zone.missions):
            if not isinstance(m, Mission):
                errors.append(f"Misión {i+1}: no es una instancia de Mission")
                continue
        for field in REQUIRED_MISSION_FIELDS:
            if getattr(m, field, None) is None:
                errors.append(f"Misión {i+1}.{field}: campo requerido")
        # New validation for validation_mode
        if getattr(m, "validation_mode", None) not in ("stdout", "return"):
            errors.append(f"Misión {i+1}.validation_mode: debe ser 'stdout' o 'return'")
        # If mode is return, expected_function must be provided and non‑empty
        if getattr(m, "validation_mode", None) == "return":
            if not getattr(m, "expected_function", None):
                errors.append(f"Misión {i+1}.expected_function: requerido cuando validation_mode='return'")
        if m.execution_mode not in ("script", "function"):
            errors.append(f"Misión {i+1}.execution_mode: debe ser 'script' o 'function'")
        if not m.test_cases:
            errors.append(f"Misión {i+1}: debe tener al menos 1 caso de prueba")
        else:
            for j, tc in enumerate(m.test_cases):
                if not isinstance(tc, TestCase):
                    errors.append(f"Misión {i+1}, caso {j+1}: no es un TestCase")

    return errors


def generate_template(author: str = "TuNombre", zone_id: int = 13) -> str:
    """Genera contenido de archivo template para nueva zona."""
    return f'''from world.zones import Zone, Mission, TestCase


# ═══════════════════════════════════════════════════════════
#  PyQuest — Zona Creada por {author}
#  Instrucciones:
#    1. Cambia el id (debe ser > 12)
#    2. Escribe la historia en story_intro
#    3. Define 5 misiones progresivas
#    4. Cada misión necesita test_cases con TestCase
#    5. Lógica opcional: style_check (pythonic score)
#    6. Guarda como zone_XX_tu_zona.py en world/zones/
#    7. El juego descubrirá tu zona automáticamente
# ═══════════════════════════════════════════════════════════

zone = Zone(
    id={zone_id},
    name="Mi Zona",
    author="{author}",
    story_intro=(
        "Escribe aquí la narrativa de tu zona.\\n"
        "Cada línea es un párrafo en la historia.\\n"
        "El tono debe coincidir con el tema Python que enseñas."
    ),
    missions=[
        Mission(
            num=1,
            title="Primera Misión",
            description="Describe qué debe hacer el jugador aquí.",
            execution_mode="script",
            code_template="print('Completa esto...')",
            test_cases=[
                TestCase(input="", expected="Salida esperada"),
            ],
            hints=[
                "Primera pista",
                "Segunda pista más específica",
            ],
        ),
        Mission(
            num=2,
            title="Segunda Misión",
            description="Más compleja que la anterior.",
            execution_mode="script",
            test_cases=[
                TestCase(input="", expected="Resultado esperado"),
            ],
        ),
        Mission(
            num=3,
            title="Tercera Misión",
            description="Combina conceptos.",
            execution_mode="function",
            code_template="def mi_funcion(param):\\n    return param",
            test_cases=[
                TestCase(input='["test"]', expected="test"),
            ],
        ),
        Mission(
            num=4,
            title="Cuarta Misión",
            description="El jugador ya domina el tema de esta zona.",
            execution_mode="function",
            test_cases=[
                TestCase(input='["a"]', expected="a"),
            ],
        ),
        Mission(
            num=5,
            title="Boss: El Reto Final",
            description="Integra todo lo aprendido en la zona.",
            execution_mode="script",
            test_cases=[
                TestCase(input="", expected="Resultado final"),
            ],
        ),
    ],
)
'''
