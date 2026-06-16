"""Descubre zonas dinámicamente leyendo el directorio world/zones/.

El engine nunca sabe cuántas zonas hay. Descubre las zonas leyendo
el directorio. Eso hace que agregar una zona — ya sea del juego o
del jugador — sea transparente al sistema. (Principio Open/Closed)
"""

import importlib.util
import sys
from pathlib import Path
from world.zones import Zone

ZONES_DIR = Path(__file__).resolve().parent / "zones"


def _import_zone_module(filepath: Path):
    module_name = filepath.stem
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def discover_zones() -> dict[int, Zone]:
    zones: dict[int, Zone] = {}
    for f in sorted(ZONES_DIR.glob("zone_*.py")):
        if f.name == "__init__.py":
            continue
        mod = _import_zone_module(f)
        if mod is None or not hasattr(mod, "zone"):
            continue
        z = mod.zone
        if isinstance(z, Zone):
            zones[z.id] = z
    return zones
