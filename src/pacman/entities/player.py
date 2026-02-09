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
    speed_multiplier: float = 1.0
    blink_on: bool = True  # used for InvincibilityBlink visual toggle
    last_move_dx: int = 1
    last_move_dy: int = 0

    def move(self, nx: int, ny: int) -> None:
        self.x = nx
        self.y = ny
