"""Tests para engine/schema.py — Validación de archivos de zona."""

import unittest
import tempfile
from pathlib import Path
from engine.schema import validate_zone_file, generate_template
from engine.schema import REQUIRED_ZONE_FIELDS, REQUIRED_MISSION_FIELDS, BUILTIN_ZONE_MAX_ID


class TestValidateZoneFile(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def _write_zone(self, content: str, name: str = "test_zone.py") -> Path:
        path = self.tmp / name
        path.write_text(content)
        return path

    def test_file_not_found(self):
        errors = validate_zone_file("/no/existe.py")
        self.assertGreater(len(errors), 0)
        self.assertIn("no encontrado", errors[0])

    def test_not_py_file(self):
        path = self._write_zone("", "zone.txt")
        errors = validate_zone_file(path)
        self.assertGreater(len(errors), 0)
        self.assertIn(".py", errors[0])

    def test_no_zone_variable(self):
        path = self._write_zone("x = 1")
        errors = validate_zone_file(path)
        self.assertGreater(len(errors), 0)
        self.assertIn("exportar `zone`", errors[0])

    def test_zone_wrong_type(self):
        path = self._write_zone("zone = 'not a Zone'")
        errors = validate_zone_file(path)
        self.assertGreater(len(errors), 0)
        self.assertIn("instancia", errors[0])

    def test_valid_template_zone(self):
        template = generate_template("Tester", zone_id=20)
        path = self._write_zone(template)
        errors = validate_zone_file(path)
        self.assertEqual(errors, [], f"Expected no errors, got: {errors}")

    def test_zone_id_too_low(self):
        template = generate_template("Tester", zone_id=5)
        path = self._write_zone(template)
        errors = validate_zone_file(path)
        self.assertGreater(len(errors), 0)

    def test_min_zone_id_accepted(self):
        template = generate_template("Tester", zone_id=13)
        path = self._write_zone(template)
        errors = validate_zone_file(path)
        # May have other mission field errors, but not id error
        id_errors = [e for e in errors if "Zone.id" in e]
        self.assertEqual(len(id_errors), 0)

    def test_syntax_error_in_zone(self):
        path = self._write_zone("zone = Zone(\n  id='broken")
        errors = validate_zone_file(path)
        self.assertGreater(len(errors), 0)


class TestGenerateTemplate(unittest.TestCase):
    def test_template_contains_author(self):
        template = generate_template("MiNombre", 20)
        self.assertIn("MiNombre", template)
        self.assertIn("20", template)

    def test_template_has_zone_var(self):
        template = generate_template()
        self.assertIn("zone = Zone(", template)

    def test_template_has_5_missions(self):
        template = generate_template()
        self.assertEqual(template.count("Mission("), 5)

    def test_template_default_values(self):
        template = generate_template()
        self.assertIn("TuNombre", template)
        self.assertIn("13", template)


class TestSchemaConstants(unittest.TestCase):
    def test_required_fields(self):
        self.assertIn("id", REQUIRED_ZONE_FIELDS)
        self.assertIn("name", REQUIRED_ZONE_FIELDS)
        self.assertIn("missions", REQUIRED_ZONE_FIELDS)

    def test_builtin_max_id(self):
        self.assertEqual(BUILTIN_ZONE_MAX_ID, 12)


if __name__ == "__main__":
    unittest.main()
