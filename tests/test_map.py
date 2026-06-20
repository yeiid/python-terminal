"""Tests para world/map.py — Mapa de zonas y navegación."""

import unittest
from world.map import (
    ZONES, get_zone, get_act_label, show_map,
    ZONE_ICONS, ACT_COLORS,
)


class TestZonesList(unittest.TestCase):
    def test_15_zones_defined(self):
        self.assertEqual(len(ZONES), 15)

    def test_all_zones_have_required_fields(self):
        for z in ZONES:
            self.assertIn("id", z)
            self.assertIn("name", z)
            self.assertIn("tema", z)
            self.assertIsInstance(z["id"], int)
            self.assertIsInstance(z["name"], str)
            self.assertIsInstance(z["tema"], str)

    def test_zone_ids_are_contiguous(self):
        ids = [z["id"] for z in ZONES]
        self.assertEqual(ids, list(range(1, 16)))

    def test_first_zone_is_barrio_base(self):
        self.assertEqual(ZONES[0]["name"], "Barrio Base")

    def test_last_zone_is_banco_de_datos(self):
        self.assertEqual(ZONES[-1]["name"], "El Banco de Datos")


class TestGetZone(unittest.TestCase):
    def test_get_first_zone(self):
        zone = get_zone(1)
        self.assertIsNotNone(zone)
        self.assertEqual(zone["name"], "Barrio Base")

    def test_get_last_builtin_zone(self):
        zone = get_zone(15)
        self.assertIsNotNone(zone)
        self.assertEqual(zone["name"], "El Banco de Datos")

    def test_get_nonexistent_zone(self):
        zone = get_zone(999)
        self.assertIsNotNone(zone)  # Returns "Zona ∞" for > 15
        self.assertEqual(zone["name"], "Zona ∞")

    def test_get_zone_0(self):
        zone = get_zone(0)
        self.assertIsNone(zone)


class TestGetActLabel(unittest.TestCase):
    def test_zone_1_label(self):
        self.assertEqual(get_act_label(1), "I")

    def test_zone_4_label(self):
        self.assertEqual(get_act_label(4), "I")

    def test_zone_5_label(self):
        self.assertEqual(get_act_label(5), "II")

    def test_zone_9_label(self):
        self.assertEqual(get_act_label(9), "II")

    def test_zone_10_label(self):
        self.assertEqual(get_act_label(10), "III")

    def test_zone_12_label(self):
        self.assertEqual(get_act_label(12), "III")

    def test_zone_13_label(self):
        self.assertEqual(get_act_label(13), "∞")

    def test_zone_99_label(self):
        self.assertEqual(get_act_label(99), "∞")


class TestZoneIcons(unittest.TestCase):
    def test_all_zones_have_icons(self):
        for z in ZONES:
            self.assertIn(z["id"], ZONE_ICONS, f"Zone {z['id']} missing icon")


class TestActColors(unittest.TestCase):
    def test_all_acts_have_colors(self):
        for act_label in ["I", "II", "III", "∞"]:
            self.assertIn(act_label, ACT_COLORS)


if __name__ == "__main__":
    unittest.main()
