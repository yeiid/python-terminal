"""Tests para engine/curriculum.py — Progreso de temas y XP."""

import unittest
import json
import os
from pathlib import Path
from engine.curriculum import (
    mark_viewed, mark_example_run, mark_practiced, mark_mastered,
    get_topic_progress, get_all_progress, get_topic_status,
    get_total_progress, get_category_progress,
    STATUS_NEW, STATUS_LEARNING, STATUS_PRACTICED, STATUS_MASTERED,
    STATUS_ICONS, STATUS_LABELS,
    XP_FIRST_VIEW, XP_EXAMPLE_RUN, XP_PRACTICED, XP_MASTERED,
    PROGRESS_FILE, _load_raw, _save_raw, TopicProgress,
)


class TestCurriculumBase(unittest.TestCase):
    def setUp(self):
        # Backup and clear progress file
        self.test_file = PROGRESS_FILE
        self.backup = None
        if self.test_file.exists():
            self.backup = self.test_file.read_text()
            self.test_file.unlink()

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()
        if self.backup:
            self.test_file.write_text(self.backup)


class TestTopicProgress(TestCurriculumBase):
    def test_default_topic_is_new(self):
        tp = get_topic_progress("variables")
        self.assertEqual(tp.status, STATUS_NEW)
        self.assertEqual(tp.xp_earned, 0)
        self.assertEqual(tp.times_viewed, 0)
        self.assertEqual(tp.examples_run, [])


class TestMarkViewed(TestCurriculumBase):
    def test_first_view_grants_xp(self):
        xp = mark_viewed("variables")
        self.assertEqual(xp, XP_FIRST_VIEW)
        tp = get_topic_progress("variables")
        self.assertEqual(tp.status, STATUS_LEARNING)
        self.assertEqual(tp.times_viewed, 1)

    def test_second_view_no_xp(self):
        mark_viewed("variables")
        xp = mark_viewed("variables")
        self.assertEqual(xp, 0)

    def test_multiple_views_increment_counter(self):
        for _ in range(5):
            mark_viewed("listas")
        tp = get_topic_progress("listas")
        self.assertEqual(tp.times_viewed, 5)


class TestMarkExampleRun(TestCurriculumBase):
    def test_first_example_grants_xp(self):
        xp = mark_example_run("listas", "Operaciones básicas")
        self.assertEqual(xp, XP_EXAMPLE_RUN)

    def test_duplicate_example_no_xp(self):
        mark_example_run("listas", "Operaciones básicas")
        xp = mark_example_run("listas", "Operaciones básicas")
        self.assertEqual(xp, 0)

    def test_new_topic_becomes_learning(self):
        mark_example_run("strings", "Métodos de string")
        tp = get_topic_progress("strings")
        self.assertEqual(tp.status, STATUS_LEARNING)
        self.assertIn("Métodos de string", tp.examples_run)

    def test_examples_tracked_separately(self):
        mark_example_run("dicts", "Ejemplo A")
        mark_example_run("dicts", "Ejemplo B")
        tp = get_topic_progress("dicts")
        self.assertEqual(len(tp.examples_run), 2)


class TestMarkPracticed(TestCurriculumBase):
    def test_new_to_practiced_grants_xp(self):
        xp = mark_practiced("variables")
        self.assertEqual(xp, XP_PRACTICED)
        tp = get_topic_progress("variables")
        self.assertEqual(tp.status, STATUS_PRACTICED)

    def test_double_practiced_no_xp(self):
        mark_practiced("variables")
        xp = mark_practiced("variables")
        self.assertEqual(xp, 0)

    def test_learning_to_practiced_grants_xp(self):
        mark_viewed("variables")
        xp = mark_practiced("variables")
        self.assertEqual(xp, XP_PRACTICED)

    def test_mastered_cannot_be_practiced(self):
        mark_mastered("variables")
        xp = mark_practiced("variables")
        self.assertEqual(xp, 0)
        tp = get_topic_progress("variables")
        self.assertEqual(tp.status, STATUS_MASTERED)


class TestMarkMastered(TestCurriculumBase):
    def test_new_to_mastered_grants_both_xp(self):
        xp = mark_mastered("variables")
        self.assertEqual(xp, XP_PRACTICED + XP_MASTERED)
        tp = get_topic_progress("variables")
        self.assertEqual(tp.status, STATUS_MASTERED)

    def test_practiced_to_mastered_grants_mastered_xp(self):
        mark_practiced("variables")
        xp = mark_mastered("variables")
        self.assertEqual(xp, XP_MASTERED)

    def test_double_mastered_no_xp(self):
        mark_mastered("variables")
        xp = mark_mastered("variables")
        self.assertEqual(xp, 0)

    def test_full_path_xp_total(self):
        mark_viewed("variables")
        mark_example_run("variables", "A")
        mark_example_run("variables", "B")
        mark_practiced("variables")
        mark_mastered("variables")
        tp = get_topic_progress("variables")
        expected = XP_FIRST_VIEW + 2 * XP_EXAMPLE_RUN + XP_PRACTICED + XP_MASTERED
        self.assertEqual(tp.xp_earned, expected)


class TestGetTopicStatus(TestCurriculumBase):
    def test_new_status(self):
        self.assertEqual(get_topic_status("variables"), STATUS_NEW)

    def test_learning_status(self):
        mark_viewed("variables")
        self.assertEqual(get_topic_status("variables"), STATUS_LEARNING)


class TestGetAllProgress(TestCurriculumBase):
    def test_empty_when_no_data(self):
        progress = get_all_progress()
        self.assertEqual(progress, {})

    def test_returns_viewed_topics(self):
        mark_viewed("variables")
        progress = get_all_progress()
        self.assertIn("variables", progress)


class TestGetTotalProgress(TestCurriculumBase):
    def test_all_new_returns_zero(self):
        completed, total, xp, pct = get_total_progress()
        self.assertEqual(completed, 0)
        self.assertGreater(total, 0)
        self.assertEqual(xp, 0)
        self.assertEqual(pct, 0)

    def test_one_completed_updates_totals(self):
        mark_mastered("variables")
        completed, total, xp, pct = get_total_progress()
        self.assertEqual(completed, 1)
        self.assertGreater(xp, 0)
        self.assertGreater(pct, 0)


class TestGetCategoryProgress(TestCurriculumBase):
    def test_fundamentos_has_6_topics(self):
        completed, total, xp = get_category_progress("Fundamentos")
        self.assertEqual(total, 6)
        self.assertEqual(completed, 0)

    def test_completed_affects_category(self):
        mark_mastered("variables")
        completed, total, xp = get_category_progress("Fundamentos")
        self.assertEqual(completed, 1)


class TestStatusIconsLabels(unittest.TestCase):
    def test_all_statuses_have_icons(self):
        for s in [STATUS_NEW, STATUS_LEARNING, STATUS_PRACTICED, STATUS_MASTERED]:
            self.assertIn(s, STATUS_ICONS)

    def test_all_statuses_have_labels(self):
        for s in [STATUS_NEW, STATUS_LEARNING, STATUS_PRACTICED, STATUS_MASTERED]:
            self.assertIn(s, STATUS_LABELS)

    def test_invalid_status_fallback(self):
        self.assertEqual(STATUS_ICONS.get("invalid", "📦"), "📦")


class TestPersistence(TestCurriculumBase):
    def test_data_saved_to_json(self):
        mark_viewed("variables")
        self.assertTrue(self.test_file.exists())
        with open(self.test_file) as f:
            data = json.load(f)
        self.assertIn("variables", data)
        self.assertEqual(data["variables"]["status"], STATUS_LEARNING)

    def test_data_loaded_correctly(self):
        mark_viewed("variables")
        mark_example_run("variables", "Test")
        raw = _load_raw()
        self.assertIn("variables", raw)
        self.assertIn("Test", raw["variables"]["examples_run"])


if __name__ == "__main__":
    unittest.main()
