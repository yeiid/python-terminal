"""Tests para world/discovery.py — Descubrimiento de zonas."""

import unittest
import tempfile
from pathlib import Path
from world.discovery import discover_zones, ZONES_DIR, _import_zone_module
from world.zones import Zone, Mission, TestCase


class TestImportZoneModule(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_import_valid_module(self):
        path = self.tmp / "test_zone.py"
        path.write_text("x = 42")
        mod = _import_zone_module(path)
        self.assertIsNotNone(mod)
        self.assertEqual(mod.x, 42)

    def test_import_nonexistent_file(self):
        path = self.tmp / "no_existe.py"
        mod = _import_zone_module(path)
        self.assertIsNone(mod)


class TestDiscoverZones(unittest.TestCase):
    def test_discovery_returns_dict(self):
        zones = discover_zones()
        self.assertIsInstance(zones, dict)

    def test_discovery_has_15_zones(self):
        zones = discover_zones()
        self.assertGreaterEqual(len(zones), 15)

    def test_zones_are_sorted_by_id(self):
        zones = discover_zones()
        ids = list(zones.keys())
        self.assertEqual(ids, sorted(ids))

    def test_zone_ids_are_contiguous_from_1(self):
        zones = discover_zones()
        ids = list(zones.keys())
        expected = list(range(1, len(ids) + 1))
        self.assertEqual(ids[:15], expected[:15])

    def test_each_zone_is_zone_instance(self):
        zones = discover_zones()
        for z in zones.values():
            self.assertIsInstance(z, Zone)

    def test_each_zone_has_missions(self):
        zones = discover_zones()
        for zid, z in zones.items():
            self.assertGreater(
                len(z.missions), 0,
                f"Zone {zid} ({z.name}) has no missions",
            )

    def test_each_zone_has_5_missions(self):
        zones = discover_zones()
        for zid, z in zones.items():
            self.assertEqual(
                len(z.missions), 5,
                f"Zone {zid} ({z.name}) has {len(z.missions)} missions, expected 5",
            )

    def test_each_mission_has_title_and_description(self):
        zones = discover_zones()
        for zid, z in zones.items():
            for m in z.missions:
                self.assertTrue(m.title, f"Zone {zid} mission {m.num} missing title")
                self.assertTrue(m.description, f"Zone {zid} mission {m.num} missing description")

    def test_each_mission_has_test_cases(self):
        zones = discover_zones()
        for zid, z in zones.items():
            for m in z.missions:
                self.assertGreater(
                    len(m.test_cases), 0,
                    f"Zone {zid} mission {m.num} has no test cases",
                )

    def test_every_mission_boss_exists(self):
        zones = discover_zones()
        for zid, z in zones.items():
            mission_nums = [m.num for m in z.missions]
            self.assertIn(5, mission_nums, f"Zone {zid} ({z.name}) missing boss mission (num=5)")

    def test_zone_has_story_intro(self):
        zones = discover_zones()
        for zid, z in zones.items():
            self.assertTrue(
                z.story_intro,
                f"Zone {zid} ({z.name}) missing story_intro",
            )

    def test_zones_dir_exists(self):
        self.assertTrue(ZONES_DIR.exists())
        self.assertTrue(ZONES_DIR.is_dir())


if __name__ == "__main__":
    unittest.main()
