from dataclasses import dataclass, field
from typing import Optional, Tuple
from .. import config

@dataclass
class Ghost:
    id: str
    x: int
    y: int
    state: str = "normal"  # normal, frightened, frozen
    ai_mode: str = "scatter"  # scatter, chase, random
    dir_dx: int = 0
    dir_dy: int = 0
    scatter_corner: Tuple[int, int] = (0, 0)  # target corner for scatter mode

    def get_valid_directions(self, level) -> list[Tuple[int, int]]:
        """Get all valid (non-wall) directions from current position."""
        candidates = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx = self.x + dx
            ny = self.y + dy
            if not level.is_wall(nx, ny):
                candidates.append((dx, dy))
        return candidates

    def is_at_intersection(self, level) -> bool:
        """Check if ghost is at an intersection (3+ valid directions)."""
        return len(self.get_valid_directions(level)) >= 3

    def choose_direction_to_target(self, level, target_x: int, target_y: int) -> None:
        """Choose direction that minimizes Manhattan distance to target.
        Implements no-reversal rule: don't reverse unless at dead end.
        """
        if self.state == "frozen":
            self.dir_dx = 0
            self.dir_dy = 0
            return

        valid_dirs = self.get_valid_directions(level)
        if not valid_dirs:
            self.dir_dx = 0
            self.dir_dy = 0
            return

        # Apply no-reversal rule: filter out opposite direction unless it's the only option
        opposite = (-self.dir_dx, -self.dir_dy)
        if len(valid_dirs) > 1 and opposite in valid_dirs:
            valid_dirs = [d for d in valid_dirs if d != opposite]

        # If current direction still valid and we're not at an intersection, keep it
        current = (self.dir_dx, self.dir_dy)
        if current in valid_dirs and not self.is_at_intersection(level):
            return

        # Choose direction that minimizes Manhattan distance to target
        best_dir = None
        best_dist = float('inf')
        for dx, dy in valid_dirs:
            nx = self.x + dx
            ny = self.y + dy
            dist = abs(nx - target_x) + abs(ny - target_y)
            # Tie-break deterministically: prefer right, left, down, up
            if dist < best_dist or (dist == best_dist and best_dir is None):
                best_dist = dist
                best_dir = (dx, dy)
            elif dist == best_dist and best_dir:
                # Tie-break order: right (1,0), left (-1,0), down (0,1), up (0,-1)
                priority_order = [(1,0), (-1,0), (0,1), (0,-1)]
                if priority_order.index((dx, dy)) < priority_order.index(best_dir):
                    best_dir = (dx, dy)

        if best_dir:
            self.dir_dx, self.dir_dy = best_dir

    def step_toward_target(self, level, target_x: int, target_y: int) -> None:
        """Move one step toward target using intelligent pathfinding."""
        if self.state == "frozen":
            return

        # Choose direction (only reconsider at intersections or when blocked)
        if self.dir_dx == 0 and self.dir_dy == 0:
            self.choose_direction_to_target(level, target_x, target_y)
        elif self.is_at_intersection(level):
            self.choose_direction_to_target(level, target_x, target_y)

        # Attempt to move
        nx = self.x + self.dir_dx
        ny = self.y + self.dir_dy
        if level.is_wall(nx, ny):
            # Blocked - force reconsideration
            self.dir_dx = 0
            self.dir_dy = 0
            return

        self.x = nx
        self.y = ny
