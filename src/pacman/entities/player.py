from dataclasses import dataclass, field
from typing import List

@dataclass
class Player:
    id: str = "player"
    x: int = 0
    y: int = 0
    dx: float = 0.0
    dy: float = 0.0
    direction: str = "RIGHT"  # Up, Down, Left, Right
    lives: int = 3
    score: int = 0
    active_powerups: List["PowerupInstance"] = field(default_factory=list)
    score_multiplier: int = 1

    def move(self, nx: int, ny: int) -> None:
        self.x = nx
        self.y = ny
