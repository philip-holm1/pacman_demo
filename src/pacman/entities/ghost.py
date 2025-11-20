from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Ghost:
    id: str
    x: int
    y: int
    state: str = "normal"  # normal, frightened, frozen
    ai_mode: str = "scatter"  # scatter, chase, random
    dir_dx: int = 0
    dir_dy: int = 0
    _decision_cooldown: int = 0  # ticks until next direction decision

    def decide_direction(self, level) -> None:
        if self.state == "frozen":
            self.dir_dx = 0
            self.dir_dy = 0
            return
        # Directions preference order to keep deterministic behavior
        candidates = [(1,0), (-1,0), (0,1), (0,-1)]
        # If current direction still valid keep it (less jitter)
        if self.dir_dx or self.dir_dy:
            nx = self.x + self.dir_dx
            ny = self.y + self.dir_dy
            if not level.is_wall(nx, ny):
                return
        for dx, dy in candidates:
            nx = self.x + dx
            ny = self.y + dy
            if not level.is_wall(nx, ny):
                self.dir_dx, self.dir_dy = dx, dy
                break
        self._decision_cooldown = 5

    def step(self, level) -> None:
        if self.state == "frozen":
            return
        if self._decision_cooldown <= 0 or (self.dir_dx == 0 and self.dir_dy == 0):
            self.decide_direction(level)
        else:
            self._decision_cooldown -= 1
        nx = self.x + self.dir_dx
        ny = self.y + self.dir_dy
        if level.is_wall(nx, ny):
            # force new decision next tick
            self.dir_dx = 0
            self.dir_dy = 0
            self._decision_cooldown = 0
            return
        self.x = nx
        self.y = ny
