from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Mission:
    num: int
    title: str
    description: str
    example: str | None = None
    code_template: str | None = None  # fill-in-the-blank
    validation_fn: Callable = lambda out, err: (False, "Not implemented")


@dataclass
class Zone:
    id: int
    name: str
    story_intro: str
    missions: list[Mission] = field(default_factory=list)
