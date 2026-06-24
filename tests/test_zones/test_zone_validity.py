import os
import sys
import unittest
from pathlib import Path


class TestZoneValidity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
        cls.zones_dir = Path(__file__).resolve().parent.parent.parent / "world" / "zones"

    def _get_zone_files(self):
        return sorted(self.zones_dir.glob("zone_*.py"))

    def _import_zone(self, filepath):
        import importlib.util
        module_name = filepath.stem
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None or spec.loader is None:
            return None, ["No se pudo crear spec"]
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            return None, [str(e)]
        if not hasattr(mod, "zone"):
            return None, ["El archivo debe exportar `zone`"]
        return mod.zone, []

    def test_all_zone_files_exist(self):
        files = self._get_zone_files()
        self.assertGreaterEqual(len(files), 15,
                                f"Se esperaban al menos 15 zonas, se encontraron {len(files)}")

    def test_each_zone_has_valid_id(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                self.fail(f"{f.name}: {errors}")
            self.assertIsInstance(zone.id, int, f"{f.name}: id debe ser entero")
            self.assertGreater(zone.id, 0, f"{f.name}: id debe ser > 0")

    def test_each_zone_has_name(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            self.assertTrue(zone.name, f"{f.name}: name no debe estar vacío")

    def test_each_zone_has_story(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            self.assertTrue(zone.story_intro, f"{f.name}: story_intro no debe estar vacío")

    def test_each_zone_has_5_missions(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            if zone.id <= 12:
                self.assertEqual(len(zone.missions), 5,
                                 f"{f.name}: esperaba 5 misiones, tiene {len(zone.missions)}")

    def test_mission_has_title_and_description(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            for m in zone.missions:
                self.assertTrue(m.title, f"{f.name} misión {m.num}: title vacío")
                self.assertTrue(m.description, f"{f.name} misión {m.num}: description vacío")

    def test_mission_has_non_empty_expected(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            for m in zone.missions:
                for i, tc in enumerate(m.test_cases):
                    if not tc.expected.strip():
                        self.fail(
                            f"{f.name} misión {m.num} caso {i + 1}: "
                            f"expected vacío. Todos los test cases deben tener expected concreto."
                        )

    def test_mission_execution_mode_valid(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            for m in zone.missions:
                self.assertIn(m.execution_mode, ("script", "function"),
                              f"{f.name} misión {m.num}: execution_mode inválido")

    def test_no_duplicate_mission_numbers(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            nums = [m.num for m in zone.missions]
            self.assertEqual(len(nums), len(set(nums)),
                             f"{f.name}: números de misión duplicados: {nums}")

    def test_mission_numbers_sequential(self):
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            nums = sorted([m.num for m in zone.missions])
            expected = list(range(1, len(nums) + 1))
            self.assertEqual(nums, expected,
                             f"{f.name}: números de misión no secuenciales: {nums}")

    def test_no_duplicate_zone_ids(self):
        seen_ids = {}
        for f in self._get_zone_files():
            zone, errors = self._import_zone(f)
            if errors:
                continue
            if zone.id in seen_ids:
                self.fail(f"id duplicado {zone.id} en {f.name} y {seen_ids[zone.id]}")
            seen_ids[zone.id] = f.name


if __name__ == "__main__":
    unittest.main()
