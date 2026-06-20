"""Tests para engine/battlepass.py — Pase de batalla y progresión."""

import unittest
from engine.battlepass import (
    get_battle_pass_tier,
    get_next_tier_info,
    get_tiers_up_to,
    get_collectible_for_zone,
    BATTLE_PASS_TIERS,
    COLLECTION_OBJECTS,
)


class TestBattlePassTier(unittest.TestCase):
    def test_tier_1_at_0_xp(self):
        self.assertEqual(get_battle_pass_tier(0), 1)

    def test_tier_1_at_199_xp(self):
        self.assertEqual(get_battle_pass_tier(199), 1)

    def test_tier_2_at_200_xp(self):
        self.assertEqual(get_battle_pass_tier(200), 2)

    def test_tier_4_at_1000_xp(self):
        self.assertEqual(get_battle_pass_tier(1000), 4)

    def test_tier_10_at_7000_xp(self):
        self.assertEqual(get_battle_pass_tier(7000), 10)

    def test_tier_10_above_max(self):
        self.assertEqual(get_battle_pass_tier(10000), 10)

    def test_negative_xp_tier_0(self):
        tier = get_battle_pass_tier(-100)
        self.assertEqual(tier, 0)


class TestNextTierInfo(unittest.TestCase):
    def test_first_tier_at_0_xp(self):
        tier, remaining, needed = get_next_tier_info(0)
        self.assertEqual(tier, 2)
        self.assertEqual(remaining, 200)
        self.assertEqual(needed, 200)

    def test_mid_progress(self):
        tier, remaining, needed = get_next_tier_info(500)
        self.assertEqual(tier, 4)
        self.assertEqual(remaining, 500)

    def test_max_tier_returns_none(self):
        tier, remaining, needed = get_next_tier_info(7000)
        self.assertIsNone(tier)
        self.assertEqual(remaining, 0)


class TestTiersUpTo(unittest.TestCase):
    def test_unlocked_count_at_0(self):
        tiers = get_tiers_up_to(0)
        unlocked = [t for t in tiers if t["unlocked"]]
        self.assertEqual(len(unlocked), 1)  # tier 1 is free

    def test_unlocked_count_at_200(self):
        tiers = get_tiers_up_to(200)
        unlocked = [t for t in tiers if t["unlocked"]]
        self.assertEqual(len(unlocked), 2)

    def test_all_tiers_returned(self):
        tiers = get_tiers_up_to(0)
        self.assertEqual(len(tiers), len(BATTLE_PASS_TIERS))


class TestBattlePassTiersData(unittest.TestCase):
    def test_tiers_in_order(self):
        for i, tier in enumerate(BATTLE_PASS_TIERS):
            self.assertEqual(tier["tier"], i + 1)

    def test_xp_requirements_increasing(self):
        xp_values = [t["xp_needed"] for t in BATTLE_PASS_TIERS]
        for i in range(1, len(xp_values)):
            self.assertGreater(xp_values[i], xp_values[i - 1])

    def test_all_tiers_have_required_fields(self):
        for tier in BATTLE_PASS_TIERS:
            self.assertIn("tier", tier)
            self.assertIn("xp_needed", tier)
            self.assertIn("reward", tier)
            self.assertIn("icon", tier)


class TestCollectibleForZone(unittest.TestCase):
    def test_zone_1_collectible(self):
        obj = get_collectible_for_zone(1)
        self.assertEqual(obj["id"], "obj_01")

    def test_zone_15_collectible(self):
        obj = get_collectible_for_zone(15)
        self.assertEqual(obj["id"], "obj_15")

    def test_zone_without_collectible(self):
        obj = get_collectible_for_zone(99)
        self.assertIsNone(obj)

    def test_every_zone_1_to_15_has_collectible(self):
        for zid in range(1, 16):
            obj = get_collectible_for_zone(zid)
            self.assertIsNotNone(obj, f"Zone {zid} missing collectible")


if __name__ == "__main__":
    unittest.main()
