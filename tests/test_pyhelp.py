"""Tests para engine/pyhelp.py — Documentación interactiva."""

import unittest
from engine.pyhelp import (
    get_topic, search_topics, TOPICS, CATEGORIES,
    PyTopic, PyExample,
)


class TestTopicData(unittest.TestCase):
    def test_18_topics_total(self):
        self.assertEqual(len(TOPICS), 18)

    def test_all_topics_have_required_fields(self):
        for t in TOPICS:
            self.assertIsInstance(t.id, str)
            self.assertIsInstance(t.title, str)
            self.assertIsInstance(t.category, str)
            self.assertIsInstance(t.icon, str)
            self.assertIsInstance(t.level, str)
            self.assertIsInstance(t.summary, str)
            self.assertIsInstance(t.content, str)
            self.assertIsInstance(t.examples, list)
            self.assertTrue(t.id, f"Topic missing id: {t.title}")
            self.assertTrue(t.title, f"Topic missing title: {t.id}")
            self.assertTrue(t.content, f"Topic missing content: {t.id}")

    def test_every_topic_has_at_least_one_example(self):
        for t in TOPICS:
            self.assertGreater(
                len(t.examples), 0,
                f"Topic '{t.id}' has no examples",
            )

    def test_examples_have_required_fields(self):
        for t in TOPICS:
            for ex in t.examples:
                self.assertIsInstance(ex, PyExample)
                self.assertTrue(ex.title, f"Example missing title in {t.id}")
                self.assertTrue(ex.code, f"Example missing code in {t.id}.{ex.title}")

    def test_valid_levels(self):
        valid = {"Principiante", "Intermedio", "Avanzado"}
        for t in TOPICS:
            self.assertIn(t.level, valid, f"Topic '{t.id}' has invalid level '{t.level}'")

    def test_valid_categories(self):
        for t in TOPICS:
            self.assertIn(
                t.category, CATEGORIES,
                f"Topic '{t.id}' has unknown category '{t.category}'",
            )

    def test_unique_ids(self):
        ids = [t.id for t in TOPICS]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate topic IDs found")


class TestGetTopic(unittest.TestCase):
    def test_get_existing_topic(self):
        t = get_topic("variables")
        self.assertIsNotNone(t)
        self.assertEqual(t.title, "Variables y Tipos de Datos")

    def test_get_another_topic(self):
        t = get_topic("listas")
        self.assertIsNotNone(t)
        self.assertEqual(t.title, "Listas")

    def test_get_nonexistent_topic(self):
        t = get_topic("no_existe")
        self.assertIsNone(t)

    def test_case_sensitivity(self):
        t = get_topic("Variables")
        self.assertIsNone(t)

    def test_all_topics_retrievable(self):
        for t in TOPICS:
            retrieved = get_topic(t.id)
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.id, t.id)


class TestSearchTopics(unittest.TestCase):
    def test_search_by_title(self):
        results = search_topics("variables")
        self.assertGreater(len(results), 0)
        self.assertTrue(any(t.id == "variables" for t in results))

    def test_search_by_summary(self):
        results = search_topics("colecciones")
        self.assertGreater(len(results), 0)

    def test_search_no_results(self):
        results = search_topics("xyzzy_nonexistent")
        self.assertEqual(len(results), 0)

    def test_search_partial(self):
        results = search_topics("lista")
        self.assertGreater(len(results), 0)
        self.assertTrue(any(t.id == "listas" for t in results))

    def test_search_case_insensitive(self):
        results_upper = search_topics("LISTAS")
        results_lower = search_topics("listas")
        self.assertEqual(len(results_upper), len(results_lower))


class TestCategories(unittest.TestCase):
    def test_expected_categories_present(self):
        expected = {"Fundamentos", "Estructuras de Datos", "Paradigmas", "IO"}
        for cat in expected:
            self.assertIn(cat, CATEGORIES)

    def test_all_topics_in_some_category(self):
        all_cat_topics = set()
        for topics in CATEGORIES.values():
            for t in topics:
                all_cat_topics.add(t.id)
        all_topic_ids = {t.id for t in TOPICS}
        self.assertEqual(all_cat_topics, all_topic_ids)

    def test_category_fundamentos_has_6_topics(self):
        self.assertEqual(len(CATEGORIES["Fundamentos"]), 6)

    def test_category_avanzado_includes_tecnicas(self):
        self.assertIn("Técnicas Avanzadas", CATEGORIES)


class TestPyTopicDataclass(unittest.TestCase):
    def test_create_topic(self):
        t = PyTopic(
            id="test", title="Test", category="Test",
            icon="🧪", level="Principiante",
            summary="A test topic", content="# Content",
        )
        self.assertEqual(t.id, "test")
        self.assertEqual(t.examples, [])

    def test_topic_with_examples(self):
        ex = PyExample(title="Ex1", code="print(1)")
        t = PyTopic(
            id="t2", title="T2", category="Cat",
            icon="📘", level="Intermedio",
            summary="S", content="C", examples=[ex],
        )
        self.assertEqual(len(t.examples), 1)
        self.assertEqual(t.examples[0].code, "print(1)")


if __name__ == "__main__":
    unittest.main()
