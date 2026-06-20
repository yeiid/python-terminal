"""Tests para engine/state.py — Estado del juego y progreso."""

import unittest
import tempfile
import json
from pathlib import Path
from engine.state import GameState, ALL_ACHIEVEMENTS, DATA_DIR


class TestGameStateInit(unittest.TestCase):
    def test_default_values(self):
        state = GameState()
        self.assertEqual(state.player_name, "Dev")
        self.assertEqual(state.level, 1)
        self.assertEqual(state.xp, 0)
        self.assertEqual(state.title, "Aprendiz")
        self.assertEqual(state.unlocked_zones, 1)
        self.assertEqual(state.completed_missions, [])
        self.assertEqual(state.achievements, [])

    def test_custom_values(self):
        state = GameState(player_name="Ana", level=5, xp=250)
        self.assertEqual(state.player_name, "Ana")
        self.assertEqual(state.level, 5)
        self.assertEqual(state.xp, 250)

    def test_xp_for_next_increases(self):
        state = GameState(level=1)
        self.assertEqual(state.xp_for_next, 100)
        state.level = 5
        self.assertEqual(state.xp_for_next, 500)

    def test_no_missions_initially(self):
        state = GameState()
        self.assertEqual(state.total_missions, 0)


class TestGameStateXP(unittest.TestCase):
    def setUp(self):
        self.state = GameState()

    def test_add_xp_increases_total(self):
        self.state.add_xp(50)
        self.assertEqual(self.state.xp, 50)
        self.assertEqual(self.state.total_xp_earned, 50)

    def test_level_up_at_100_xp(self):
        self.state.add_xp(100)
        self.assertEqual(self.state.level, 2)
        self.assertEqual(self.state.xp, 0)

    def test_level_up_with_remaining_xp(self):
        self.state.add_xp(250)
        self.assertGreaterEqual(self.state.level, 2)
        self.assertEqual(self.state.xp, 250 - 100)

    def test_level_5_title_dev(self):
        # Need cumulative XP: 100+200+300+400+500 = 1500+? Actually just add enough
        self.state.add_xp(2000)
        self.assertGreaterEqual(self.state.level, 5,
            f"Level {self.state.level} should be >= 5")
        self.assertEqual(self.state.title, "Dev")

    def test_level_10_title_senior(self):
        self.state.add_xp(10000)
        self.assertGreaterEqual(self.state.level, 10,
            f"Level {self.state.level} should be >= 10")
        self.assertEqual(self.state.title, "Senior")

    def test_negative_xp_does_not_affect_total(self):
        self.state.add_xp(100)
        total_before = self.state.total_xp_earned
        self.state.add_xp(-50)
        self.assertEqual(self.state.total_xp_earned, total_before)

    def test_level_up_triggers_achievement(self):
        self.state.add_xp(2000)
        self.assertIn("nivel_5", self.state.achievements)

    def test_xp_progress_float(self):
        self.state.add_xp(50)
        self.assertAlmostEqual(self.state.xp_progress, 0.5)


class TestGameStateMissions(unittest.TestCase):
    def setUp(self):
        self.state = GameState()

    def test_complete_mission(self):
        self.state.completed_missions.append("1-1")
        self.assertEqual(self.state.total_missions, 1)

    def test_completed_zones(self):
        self.state.completed_missions.extend(["1-1", "1-2", "2-1"])
        zones = self.state.completed_zones
        self.assertIn(1, zones)
        self.assertIn(2, zones)
        self.assertNotIn(3, zones)

    def test_mission_achievement_10(self):
        for z in range(1, 4):
            for m in range(1, 5):
                self.state.completed_missions.append(f"{z}-{m}")
        self.state.check_mission_achievements(1)
        self.assertIn("diez_misiones", self.state.achievements)

    def test_zone_complete_achievement(self):
        for m in range(1, 6):
            self.state.completed_missions.append(f"1-{m}")
        self.state.check_zone_complete(1)
        self.assertIn("zona_completa", self.state.achievements)


class TestGameStateAchievements(unittest.TestCase):
    def setUp(self):
        self.state = GameState()

    def test_add_achievement_once(self):
        self.state.add_achievement("primera_mision")
        self.assertEqual(len(self.state.achievements), 1)
        self.state.add_achievement("primera_mision")
        self.assertEqual(len(self.state.achievements), 1, "No debe duplicar")

    def test_invalid_achievement_ignored(self):
        self.state.add_achievement("no_existe")
        self.assertEqual(len(self.state.achievements), 0)

    def test_all_achievements_defined(self):
        required = [
            "primera_mision", "diez_misiones", "nivel_5", "nivel_10",
            "creador", "primer_acto", "boss_hunter",
        ]
        for ach in required:
            self.assertIn(ach, ALL_ACHIEVEMENTS)


class TestGameStatePersistence(unittest.TestCase):
    def setUp(self):
        # Backup original save
        self.orig_path = DATA_DIR / "player_save.json"
        self.orig_data = None
        if self.orig_path.exists():
            self.orig_data = self.orig_path.read_text()

    def tearDown(self):
        # Restore original save
        if self.orig_data:
            self.orig_path.write_text(self.orig_data)
        elif self.orig_path.exists():
            self.orig_path.unlink()

    def test_save_and_load_roundtrip(self):
        state = GameState(player_name="TestUser", level=3, xp=150)
        state.completed_missions = ["1-1", "1-2"]
        state.achievements = ["primera_mision"]
        state.save()

        loaded = GameState.load()
        self.assertEqual(loaded.player_name, "TestUser")
        self.assertEqual(loaded.level, 3)
        self.assertEqual(loaded.xp, 150)
        self.assertEqual(loaded.total_missions, 2)
        self.assertIn("primera_mision", loaded.achievements)

    def test_load_default_when_no_file(self):
        if self.orig_path.exists():
            self.orig_path.unlink()
        state = GameState.load()
        self.assertEqual(state.player_name, "Dev")

    def test_save_creates_file(self):
        state = GameState(player_name="SaveTest")
        state.save()
        self.assertTrue(self.orig_path.exists())
        with open(self.orig_path) as f:
            data = json.load(f)
        self.assertEqual(data["player_name"], "SaveTest")


class TestGameStateHints(unittest.TestCase):
    def setUp(self):
        self.state = GameState()

    def test_hints_used_in_zone_starts_zero(self):
        self.assertEqual(self.state.get_hints_used_in_zone(1), 0)

    def test_hints_used_in_zone_tracks(self):
        self.state.hints_used_in_zone["1"] = 3
        self.assertEqual(self.state.get_hints_used_in_zone(1), 3)

    def test_zone_xp_tracking(self):
        self.state.add_xp_to_zone(1, 100)
        self.state.add_xp_to_zone(1, 50)
        self.assertEqual(self.state.xp_per_zone["1"], 150)

    def test_play_time_accumulates(self):
        self.state.session_start = 0
        self.state.total_play_time = 3600
        self.state.save()
        loaded = GameState.load()
        self.assertGreaterEqual(loaded.total_play_time, 3600)


if __name__ == "__main__":
    unittest.main()
