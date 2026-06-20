"""Sistema de progreso de aprendizaje de PyQuest.

Registra el avance del estudiante en cada tema de la documentación:
  - Ejecución de ejemplos (automático)
  - Estado: Nuevo → Estudiando → Practicado → Dominado (manual+automático)
  - XP por progreso
"""

import json
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROGRESS_FILE = DATA_DIR / "topic_progress.json"

STATUS_NEW = "new"
STATUS_LEARNING = "learning"
STATUS_PRACTICED = "practiced"
STATUS_MASTERED = "mastered"

STATUS_ICONS = {
    STATUS_NEW: "📦",
    STATUS_LEARNING: "📖",
    STATUS_PRACTICED: "✅",
    STATUS_MASTERED: "⭐",
}

STATUS_LABELS = {
    STATUS_NEW: "Nuevo",
    STATUS_LEARNING: "Estudiando",
    STATUS_PRACTICED: "Practicado",
    STATUS_MASTERED: "Dominado",
}


@dataclass
class TopicProgress:
    topic_id: str = ""
    status: str = STATUS_NEW
    examples_run: list[str] = field(default_factory=list)
    times_viewed: int = 0
    last_viewed: str = ""
    xp_earned: int = 0


XP_FIRST_VIEW = 5
XP_EXAMPLE_RUN = 10
XP_PRACTICED = 20
XP_MASTERED = 50


def _load_raw() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}


def _save_raw(data: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _get_topic_data(topic_id: str) -> TopicProgress:
    data = _load_raw()
    raw = data.get(topic_id, {})
    raw.pop("topic_id", None)
    return TopicProgress(topic_id=topic_id, **raw)


def _put_topic_data(tp: TopicProgress):
    data = _load_raw()
    data[tp.topic_id] = asdict(tp)
    _save_raw(data)


def get_all_progress() -> dict[str, TopicProgress]:
    data = _load_raw()
    result = {}
    for tid, raw in data.items():
        raw.pop("topic_id", None)
        result[tid] = TopicProgress(topic_id=tid, **raw)
    return result


def get_topic_status(topic_id: str) -> str:
    tp = _get_topic_data(topic_id)
    return tp.status


def mark_viewed(topic_id: str) -> int:
    """Marca un tema como visto. Retorna XP ganado (0 o XP_FIRST_VIEW)."""
    tp = _get_topic_data(topic_id)
    was_new = tp.status == STATUS_NEW
    tp.times_viewed += 1
    tp.last_viewed = time.strftime("%Y-%m-%d %H:%M")
    if was_new:
        tp.status = STATUS_LEARNING
        tp.xp_earned += XP_FIRST_VIEW
        _put_topic_data(tp)
        return XP_FIRST_VIEW
    _put_topic_data(tp)
    return 0


def mark_example_run(topic_id: str, example_title: str) -> int:
    """Marca un ejemplo como ejecutado. Retorna XP ganado."""
    tp = _get_topic_data(topic_id)
    if tp.status == STATUS_NEW:
        tp.status = STATUS_LEARNING
    if example_title not in tp.examples_run:
        tp.examples_run.append(example_title)
        tp.xp_earned += XP_EXAMPLE_RUN
        tp.last_viewed = time.strftime("%Y-%m-%d %H:%M")
        _put_topic_data(tp)
        return XP_EXAMPLE_RUN
    return 0


def mark_practiced(topic_id: str) -> int:
    """Marca un tema como Practicado. Retorna XP ganado."""
    tp = _get_topic_data(topic_id)
    old_status = tp.status
    if old_status in (STATUS_MASTERED,):
        return 0
    tp.status = STATUS_PRACTICED
    tp.last_viewed = time.strftime("%Y-%m-%d %H:%M")
    gained = 0
    if old_status != STATUS_PRACTICED:
        tp.xp_earned += XP_PRACTICED
        gained = XP_PRACTICED
    _put_topic_data(tp)
    return gained


def mark_mastered(topic_id: str) -> int:
    """Marca un tema como Dominado. Retorna XP ganado."""
    tp = _get_topic_data(topic_id)
    old_status = tp.status
    if old_status == STATUS_MASTERED:
        return 0
    if old_status != STATUS_PRACTICED:
        tp.status = STATUS_PRACTICED
        tp.xp_earned += XP_PRACTICED
    tp.status = STATUS_MASTERED
    tp.xp_earned += XP_MASTERED
    tp.last_viewed = time.strftime("%Y-%m-%d %H:%M")
    gained = XP_MASTERED + (XP_PRACTICED if old_status != STATUS_PRACTICED else 0)
    _put_topic_data(tp)
    return gained


def get_topic_progress(topic_id: str) -> TopicProgress:
    return _get_topic_data(topic_id)


def get_category_progress(category: str) -> tuple[int, int, int]:
    """Retorna (completados, total, xp_total) para una categoría."""
    from engine.pyhelp import CATEGORIES, TOPICS

    topics_in_cat = CATEGORIES.get(category, [])
    total = len(topics_in_cat)
    completed = 0
    xp_total = 0
    for t in topics_in_cat:
        tp = _get_topic_data(t.id)
        xp_total += tp.xp_earned
        if tp.status in (STATUS_PRACTICED, STATUS_MASTERED):
            completed += 1
    return completed, total, xp_total


def get_total_progress() -> tuple[int, int, int, int]:
    """Retorna (completados, total, xp_total, pct)."""
    from engine.pyhelp import TOPICS

    total = len(TOPICS)
    completed = 0
    xp_total = 0
    for t in TOPICS:
        tp = _get_topic_data(t.id)
        xp_total += tp.xp_earned
        if tp.status in (STATUS_PRACTICED, STATUS_MASTERED):
            completed += 1
    pct = int((completed / total) * 100) if total else 0
    return completed, total, xp_total, pct


def get_topic_status_icon(status: str) -> str:
    return STATUS_ICONS.get(status, "📦")


def get_topic_status_label(status: str) -> str:
    return STATUS_LABELS.get(status, "Nuevo")
