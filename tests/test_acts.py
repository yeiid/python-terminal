"""Tests para engine/acts.py — Sistema de Actos y reglas del juego."""

import unittest
from engine.acts import get_act, Act, ACTS


class TestActDetection(unittest.TestCase):
    def test_zone_1_is_act_1(self):
        act = get_act(1)
        self.assertEqual(act.id, "I")

    def test_zone_4_is_act_1(self):
        act = get_act(4)
        self.assertEqual(act.id, "I")

    def test_zone_5_is_act_2(self):
        act = get_act(5)
        self.assertEqual(act.id, "II")

    def test_zone_9_is_act_2(self):
        act = get_act(9)
        self.assertEqual(act.id, "II")

    def test_zone_10_is_act_3(self):
        act = get_act(10)
        self.assertEqual(act.id, "III")

    def test_zone_12_is_act_3(self):
        act = get_act(12)
        self.assertEqual(act.id, "III")

    def test_zone_13_is_infinity(self):
        act = get_act(13)
        self.assertEqual(act.id, "∞")

    def test_zone_99_is_infinity(self):
        act = get_act(99)
        self.assertEqual(act.id, "∞")

    def test_zone_0_returns_infinity(self):
        act = get_act(0)
        self.assertEqual(act.id, "∞")

    def test_negative_zone_returns_infinity(self):
        act = get_act(-1)
        self.assertEqual(act.id, "∞")


class TestActProperties(unittest.TestCase):
    def test_act_1_has_unlimited_hints(self):
        act = get_act(1)
        self.assertEqual(act.max_hints_per_mission, -1)

    def test_act_1_requires_code_template(self):
        act = get_act(1)
        self.assertTrue(act.code_template_required)

    def test_act_1_xp_multiplier(self):
        act = get_act(1)
        self.assertEqual(act.xp_multiplier, 1.0)

    def test_act_2_limited_hints(self):
        act = get_act(5)
        self.assertEqual(act.max_hints_per_mission, 3)

    def test_act_2_no_code_template_required(self):
        act = get_act(5)
        self.assertFalse(act.code_template_required)

    def test_act_2_xp_multiplier(self):
        act = get_act(5)
        self.assertEqual(act.xp_multiplier, 1.5)

    def test_act_3_no_hints(self):
        act = get_act(10)
        self.assertEqual(act.max_hints_per_mission, 0)

    def test_act_3_no_skip(self):
        act = get_act(10)
        self.assertFalse(act.allow_skip_with_penalty)

    def test_act_3_xp_multiplier(self):
        act = get_act(10)
        self.assertEqual(act.xp_multiplier, 2.0)

    def test_act_inf_xp_multiplier(self):
        act = get_act(13)
        self.assertEqual(act.xp_multiplier, 3.0)

    def test_act_inf_unlimited_hints(self):
        act = get_act(13)
        self.assertEqual(act.max_hints_per_mission, -1)


class TestActsList(unittest.TestCase):
    def test_four_acts_total(self):
        self.assertEqual(len(ACTS), 4)

    def test_acts_have_all_fields(self):
        for act in ACTS:
            self.assertIsInstance(act.id, str)
            self.assertIsInstance(act.name, str)
            self.assertIsInstance(act.zone_range, tuple)
            self.assertEqual(len(act.zone_range), 2)
            self.assertIsInstance(act.color, str)
            self.assertIsInstance(act.description, str)
            self.assertIsInstance(act.max_hints_per_mission, int)
            self.assertIsInstance(act.code_template_required, bool)
            self.assertIsInstance(act.allow_skip_with_penalty, bool)
            self.assertIsInstance(act.xp_multiplier, float)

    def test_no_overlapping_ranges(self):
        ranges = [act.zone_range for act in ACTS]
        for i, r1 in enumerate(ranges):
            for j, r2 in enumerate(ranges):
                if i < j:
                    msg = f"Overlap between act {i} range {r1} and act {j} range {r2}"
                    self.assertFalse(r1[1] >= r2[0] and r2[1] >= r1[0], msg)

    def test_acts_in_order(self):
        ids = [act.id for act in ACTS]
        self.assertEqual(ids, ["I", "II", "III", "∞"])


if __name__ == "__main__":
    unittest.main()
