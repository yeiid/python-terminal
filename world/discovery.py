"""Descubre zonas dinámicamente leyendo el directorio world/zones/.

El engine nunca sabe cuántas zonas hay. Descubre las zonas leyendo
el directorio. El orden lo determina el campo `id` de la metadata
de cada zona, no el nombre del archivo.

Si dos zonas tienen el mismo id, el engine lanza un error visible
y se queda con la última cargada.
"""

import importlib.util
import sys
from pathlib import Path
from world.zones import Zone

ZONES_DIR = Path(__file__).resolve().parent / "zones"


def _import_zone_module(filepath: Path):
    if not filepath.exists():
        return None
    module_name = filepath.stem
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod


def discover_zones() -> dict[int, Zone]:
    """Escanea world/zones/ y retorna dict {id: Zone} ordenado por id.

    Si detecta ids duplicados, imprime advertencia y usa el último.
    """
    from engine.console import console

    zones: dict[int, Zone] = {}
    errors: list[str] = []

    for f in sorted(ZONES_DIR.glob("zone_*.py")):
        if f.name == "__init__.py":
            continue
        mod = _import_zone_module(f)
        if mod is None or not hasattr(mod, "zone"):
            continue
        z = mod.zone
        if not isinstance(z, Zone):
            errors.append(f"{f.name}: `zone` no es una instancia de Zone")
            continue
        if not hasattr(z, "id") or z.id is None:
            errors.append(f"{f.name}: la zona no tiene campo `id`")
            continue
        if z.id in zones:
            console.print(
                f"[yellow]⚠ Dos zonas con id={z.id}: "
                f"'{zones[z.id].name}' y '{z.name}'. "
                f"Usando la última.[/]"
            )
        zones[z.id] = z

    for err in errors:
        console.print(f"[red]✗ {err}[/]")

    return dict(sorted(zones.items()))
