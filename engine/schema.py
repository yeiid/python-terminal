"""Validador de esquemas para zonas de PyQuest.

Permite validar zonas creadas por jugadores (Zona ∞) contra el schema
del engine. También genera templates para nuevas zonas.
"""

import importlib.util
import sys
from pathlib import Path
from world.zones import Zone, Mission

REQUIRED_ZONE_FIELDS = {"id", "name", "story_intro", "missions"}
REQUIRED_MISSION_FIELDS = {"num", "title", "description"}


def validate_zone_file(filepath: str | Path) -> list[str]:
    """Valida un archivo de zona contra el schema del engine.
    Retorna lista de errores (vacía si es válido)."""
    errors = []
    filepath = Path(filepath)

    if not filepath.exists():
        return [f"Archivo no encontrado: {filepath}"]
    if filepath.suffix != ".py":
        return [f"Debe ser un archivo .py, no {filepath.suffix}"]

    module_name = filepath.stem
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None or spec.loader is None:
        return [f"No se pudo cargar {filepath}"]

    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return [f"Error de importación: {e}"]

    if not hasattr(mod, "zone"):
        return ["El archivo debe exportar una variable `zone`"]

    zone = mod.zone
    if not isinstance(zone, Zone):
        return ["`zone` debe ser una instancia de la dataclass Zone"]

    for field in REQUIRED_ZONE_FIELDS:
        if not hasattr(zone, field) or getattr(zone, field) is None:
            errors.append(f"Campo faltante en Zone: {field}")

    if hasattr(zone, "id") and zone.id < 13:
        errors.append(f"El ID de zona debe ser >= 13 (las zonas 1-12 son del juego base). ID actual: {zone.id}")

    if not zone.missions:
        errors.append("La zona debe tener al menos 1 misión")
    else:
        for i, m in enumerate(zone.missions):
            if not isinstance(m, Mission):
                errors.append(f"Misión {i+1}: no es una instancia válida de Mission")
                continue
            for field in REQUIRED_MISSION_FIELDS:
                if not hasattr(m, field) or getattr(m, field) is None:
                    errors.append(f"Misión {i+1}: campo faltante {field}")

        if len(zone.missions) > 10:
            errors.append("Máximo 10 misiones por zona")

    return errors


def generate_template(author: str = "TuNombre") -> str:
    """Genera el contenido de un archivo template para nueva zona."""
    return f'''from world.zones import Zone, Mission


# ═══════════════════════════════════════════════════
#  PyQuest — Zona Creada por {author}
#  Instrucciones:
#    1. Cambia el ID (debe ser >= 13)
#    2. Escribe la historia en story_intro
#    3. Define 5 misiones progresivas
#    4. Cada misión necesita una validation_fn
#    5. Guarda como zone_XX_tu_zona.py en world/zones/
#    6. El juego descubrirá tu zona automáticamente
# ═══════════════════════════════════════════════════

zone = Zone(
    id=13,
    name="Mi Zona",
    story_intro=(
        "Escribe aquí la narrativa de tu zona.\\n"
        "Cada línea es un párrafo en la historia.\\n"
        "El tone debe coincidir con el tema Python que enseñas."
    ),
    missions=[
        Mission(
            num=1,
            title="Primera Misión",
            description="Describe qué debe hacer el jugador aquí.",
            example="print('Ejemplo de código')",
            validation_fn=lambda out, err: (
                "resultado esperado" in out,
                "Mensaje si falla"
            ),
        ),
        Mission(
            num=2,
            title="Segunda Misión",
            description="Más compleja que la anterior.",
            validation_fn=lambda out, err: (True, ""),
        ),
        Mission(
            num=3,
            title="Tercera Misión",
            description="El jugador ya debería estar familiarizado con el tema.",
            validation_fn=lambda out, err: (True, ""),
        ),
        Mission(
            num=4,
            title="Cuarta Misión",
            description="Combina conceptos aprendidos en la zona.",
            validation_fn=lambda out, err: (True, ""),
        ),
        Mission(
            num=5,
            title="Boss: El Reto Final",
            description="La misión más difícil de la zona. Integra todo lo aprendido.",
            validation_fn=lambda out, err: (True, ""),
        ),
    ],
)
'''
