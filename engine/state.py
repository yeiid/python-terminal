from dataclasses import dataclass, asdict
import json
import time
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"

ALL_ACHIEVEMENTS = {
    "primera_mision":      {"name": "Primer Paso",      "icon": "🌟", "desc": "Completar tu primera misión"},
    "diez_misiones":       {"name": "Estudiante",       "icon": "📚", "desc": "Completar 10 misiones"},
    "treinta_misiones":    {"name": "Dedicado",         "icon": "🔥", "desc": "Completar 30 misiones"},
    "todas_misiones":      {"name": "Completista",      "icon": "🏆", "desc": "Completar las 60 misiones"},
    "zona_completa":       {"name": "Conquistador",     "icon": "🗺️", "desc": "Completar una zona entera sin saltos"},
    "todas_zonas":         {"name": "Explorador",       "icon": "🌍", "desc": "Desbloquear las 12 zonas"},
    "boss_hunter":         {"name": "Cazador de Bosses","icon": "🎯", "desc": "Completar todas las misiones Boss"},
    "one_liner":           {"name": "One Liner",        "icon": "⚡", "desc": "Resolver una misión en 1 línea"},
    "speed_run":           {"name": "Speed Run",        "icon": "💨", "desc": "Completar una misión en <30s"},
    "no_hints":            {"name": "Sin Pistas",       "icon": "🧠", "desc": "Completar una zona sin pedir hints"},
    "nivel_5":             {"name": "Dev",              "icon": "⭐", "desc": "Alcanzar nivel 5"},
    "nivel_10":            {"name": "Senior",           "icon": "💎", "desc": "Alcanzar nivel 10"},
    "nivel_15":            {"name": "Arquitecto",       "icon": "🔮", "desc": "Alcanzar nivel 15"},
    "nivel_20":            {"name": "Legendario",       "icon": "👑", "desc": "Alcanzar nivel 20"},
}


@dataclass
class GameState:
    player_name: str = "Dev"
    level: int = 1
    xp: int = 0
    title: str = "Aprendiz"
    total_xp_earned: int = 0
    unlocked_zones: int = 1
    completed_missions: list[str] = None
    achievements: list[str] = None
    hints_used: int = 0
    missions_skipped: int = 0
    total_play_time: float = 0.0
    session_start: float = 0.0

    def __post_init__(self):
        if self.completed_missions is None:
            self.completed_missions = []
        if self.achievements is None:
            self.achievements = []
        if self.session_start == 0.0:
            self.session_start = time.time()

    @property
    def xp_for_next(self) -> int:
        return self.level * 100

    @property
    def xp_progress(self) -> float:
        return self.xp / self.xp_for_next if self.xp_for_next > 0 else 0

    @property
    def total_missions(self) -> int:
        return len(self.completed_missions)

    @property
    def completed_zones(self) -> set[int]:
        zones = set()
        for m in self.completed_missions:
            zid = m.split("-")[0]
            zones.add(int(zid))
        return zones

    def add_xp(self, amount: int):
        self.xp += amount
        if amount > 0:
            self.total_xp_earned += amount
        while self.xp >= self.xp_for_next:
            self.xp -= self.xp_for_next
            self.level += 1
            self._update_title()
        self._check_level_achievements()

    def _update_title(self):
        if self.level >= 20:
            self.title = "Legend"
        elif self.level >= 15:
            self.title = "Architect"
        elif self.level >= 10:
            self.title = "Senior"
        elif self.level >= 5:
            self.title = "Dev"

    def _check_level_achievements(self):
        level_ach = {5: "nivel_5", 10: "nivel_10", 15: "nivel_15", 20: "nivel_20"}
        for lv, ach in level_ach.items():
            if self.level >= lv:
                self.add_achievement(ach)

    def add_achievement(self, name: str):
        if name in ALL_ACHIEVEMENTS and name not in self.achievements:
            self.achievements.append(name)

    def check_mission_achievements(self, zone_id: int):
        if len(self.completed_missions) == 1:
            self.add_achievement("primera_mision")
        if len(self.completed_missions) >= 10:
            self.add_achievement("diez_misiones")
        if len(self.completed_missions) >= 30:
            self.add_achievement("treinta_misiones")
        if len(self.completed_missions) >= 60:
            self.add_achievement("todas_misiones")

        zone_missions = [m for m in self.completed_missions if m.startswith(f"{zone_id}-")]
        if len(zone_missions) == 5 and self.hints_used_in_zone(zone_id) == 0:
            self.add_achievement("no_hints")

        if self.unlocked_zones >= 12:
            self.add_achievement("todas_zonas")

    def hints_used_in_zone(self, zone_id: int) -> int:
        return 0

    def check_zone_complete(self, zone_id: int):
        zone_missions = [m for m in self.completed_missions if m.startswith(f"{zone_id}-")]
        if len(zone_missions) == 5:
            self.add_achievement("zona_completa")

    def check_boss_hunter(self):
        bosses = [f"{z}-5" for z in range(1, 13)]
        if all(b in self.completed_missions for b in bosses):
            self.add_achievement("boss_hunter")

    def get_medals(self) -> list[dict]:
        return [
            {"id": k, **ALL_ACHIEVEMENTS[k], "unlocked": k in self.achievements}
            for k in ALL_ACHIEVEMENTS
        ]

    def save(self):
        if self.session_start:
            self.total_play_time += time.time() - self.session_start
            self.session_start = time.time()
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(DATA_DIR / "player_save.json", "w") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls) -> "GameState":
        path = DATA_DIR / "player_save.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            return cls(**data)
        return cls()
