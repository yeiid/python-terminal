"""Tests para engine/collection.py — Sistema de colección de objetos."""

import unittest
from engine.collection import (
    check_zone_object_unlocked,
    try_collect_object,
    _get_obj_for_zone,
)
from engine.battlepass import COLLECTION_OBJECTS


class TestGetObjForZone(unittest.TestCase):
    def test_zone_1_has_object(self):
        obj = _get_obj_for_zone(1)
        self.assertIsNotNone(obj)
        self.assertEqual(obj["name"], "Variable Espectral")

    def test_zone_15_has_object(self):
        obj = _get_obj_for_zone(15)
        self.assertIsNotNone(obj)
        self.assertEqual(obj["name"], "Datos del Origen")

    def test_zone_99_has_no_object(self):
        obj = _get_obj_for_zone(99)
        self.assertIsNone(obj)

    def test_all_objects_have_required_fields(self):
        for obj in COLLECTION_OBJECTS:
            self.assertIn("id", obj)
            self.assertIn("name", obj)
            self.assertIn("zone_id", obj)
            self.assertIn("icon", obj)
            self.assertIn("desc", obj)
            self.assertIsInstance(obj["zone_id"], int)


class TestCheckZoneObjectUnlocked(unittest.TestCase):
    def test_not_unlocked_with_few_missions(self):
        result = check_zone_object_unlocked(1, ["1-1", "1-2"], [])
        self.assertFalse(result)

    def test_unlocked_with_3_missions(self):
        result = check_zone_object_unlocked(1, ["1-1", "1-2", "1-3"], [])
        self.assertTrue(result)

    def test_already_collected(self):
        result = check_zone_object_unlocked(1, [], ["obj_01"])
        self.assertTrue(result)

    def test_no_object_for_zone(self):
        result = check_zone_object_unlocked(99, ["99-1", "99-2", "99-3"], [])
        self.assertFalse(result)

    def test_missions_from_other_zone_dont_count(self):
        result = check_zone_object_unlocked(1, ["2-1", "2-2", "2-3"], [])
        self.assertFalse(result)


class TestTryCollectObject(unittest.TestCase):
    def test_collect_with_3_missions(self):
        collected = []
        result = try_collect_object(1, ["1-1", "1-2", "1-3"], collected)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Variable Espectral")
        self.assertIn("obj_01", collected)

    def test_no_collect_with_2_missions(self):
        collected = []
        result = try_collect_object(1, ["1-1", "1-2"], collected)
        self.assertIsNone(result)
        self.assertEqual(len(collected), 0)

    def test_no_double_collect(self):
        collected = ["obj_01"]
        result = try_collect_object(1, ["1-1", "1-2", "1-3"], collected)
        self.assertIsNone(result)

    def test_collect_no_object_for_zone(self):
        collected = []
        result = try_collect_object(99, ["99-1", "99-2", "99-3"], collected)
        self.assertIsNone(result)

    def test_collect_each_zone_once(self):
        collected = []
        for zone_id in range(1, 16):
            missions = [f"{zone_id}-{m}" for m in range(1, 6)]
            result = try_collect_object(zone_id, missions, collected)
            if _get_obj_for_zone(zone_id):
                self.assertIsNotNone(result)
        self.assertEqual(len(collected), 15)


if __name__ == "__main__":
    unittest.main()
