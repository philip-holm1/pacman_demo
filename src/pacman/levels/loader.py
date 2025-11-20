import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

@dataclass
class Level:
    id: str
    width: int
    height: int
    tile_grid: List[str]
    pellet_positions: List[Dict[str, int]]
    ghost_spawn_points: List[Dict[str, int]]
    player_spawn: Dict[str, int]

    def is_wall(self, x: int, y: int) -> bool:
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            return True
        return self.tile_grid[y][x] == "#"


def load_level(path: str) -> Level:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data: Any = json.load(f)
    return Level(
        id=data["id"],
        width=data["width"],
        height=data["height"],
        tile_grid=data["tile_grid"],
        pellet_positions=data.get("pellet_positions", []),
        ghost_spawn_points=data.get("ghost_spawn_points", []),
        player_spawn=data.get("player_spawn", {"x": 0, "y": 0}),
    )
