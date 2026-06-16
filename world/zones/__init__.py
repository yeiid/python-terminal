"""Schema de zona — el contrato más crítico de PyQuest.

Todo depende de esto: el validator, el renderer, el executor,
y las zonas del usuario. Los tipos son precisos y documentados.
"""

from dataclasses import dataclass, field, asdict
from typing import Callable


@dataclass
class TestCase:
    """Un caso de prueba para una misión.

    Si execution_mode es "script":
        input_str se pasa por stdin, expected se compara con stdout.
    Si execution_mode es "function":
        input_str se usa como argumento a la función, expected es el
        valor de retorno esperado convertido a string.
    """
    input: str = ""
    expected: str = ""


@dataclass
class ExecutionResult:
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False
    exit_code: int = 0


@dataclass
class Mission:
    """Una misión dentro de una zona.

    Todas las misiones tienen descripción. El code_template es
    obligatorio en Acto I, opcional en Acto II, inexistente en Acto III.
    Los hints se revelan uno a la vez en orden.
    """
    num: int                           # Número de misión (1-5 normalmente)
    title: str                         # Título corto
    description: str                   # Qué debe hacer el jugador
    execution_mode: str = "script"     # "script" | "function"
    validation_mode: str = "stdout"   # "stdout" | "return"
    expected_function: str | None = None   # name of function when mode == "return"
    code_template: str | None = None   # Código base para completar
    test_cases: list[TestCase] = field(default_factory=lambda: [TestCase()])
    hints: list[str] = field(default_factory=list)
    style_check: Callable | None = None  # Evalúa si es pythonic → float 0-1
    xp_reward: int = 0                 # 0 = calculado automático (num * 20)

    def __post_init__(self):
        if self.xp_reward == 0:
            self.xp_reward = self.num * 20
        if not self.test_cases:
            self.test_cases = [TestCase()]


@dataclass
class Zone:
    """Una zona completa de PyQuest.

    El id determina el orden en el mapa y la detección de duplicados.
    author = None para zonas built-in del juego base.
    """
    id: int
    name: str
    story_intro: str
    missions: list[Mission] = field(default_factory=list)
    author: str | None = None
    xp_bonus: int = 0
