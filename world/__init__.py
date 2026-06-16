"""World package — el mapa y las zonas de PyQuest City.

Las zonas se descubren automáticamente desde world/zones/.
Si agregas un archivo zone_*.py con una variable `zone`,
el engine lo cargará sin tocar nada más.
"""

from world.map import ZONES, show_map, get_zone
from world.discovery import discover_zones

ZONE_CLASSES = discover_zones()
ZONE_CLASSES = dict(sorted(ZONE_CLASSES.items()))

__all__ = ["ZONES", "show_map", "get_zone", "ZONE_CLASSES"]
