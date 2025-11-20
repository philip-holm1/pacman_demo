from dataclasses import dataclass, field
from typing import List, Optional
from ..entities.player import Player
from ..entities.ghost import Ghost
from ..levels.loader import Level
from .. import config
from ..levels.loader import load_level
from .event_bus import EventBus

@dataclass
class GameState:
    level: Level
    player: Player
    ghosts: List[Ghost] = field(default_factory=list)
    tick_count: int = 0
    paused: bool = False
    mode: str = "playing"  # playing | victory | game_over
    level_source_path: Optional[str] = None
    event_bus: EventBus = field(default_factory=EventBus)
    consumed_pellets: int = 0
    high_score: int = 0
    high_score_path: Optional[str] = "data/highscore.json"
    floating_feedback: List[dict] = field(default_factory=list)

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def tick(self) -> None:
        if not self.paused:
            self.tick_count += 1

    def restart(self) -> None:
        if self.level_source_path:
            self.level = load_level(self.level_source_path)
        # reset player state
        self.player.x = self.level.player_spawn.get("x", 0)
        self.player.y = self.level.player_spawn.get("y", 0)
        self.player.lives = config.START_LIVES
        self.player.score = 0
        self.player.active_powerups.clear()
        self.ghosts.clear()
        # Respawn ghosts from level spawn points
        for i, sp in enumerate(self.level.ghost_spawn_points):
            self.ghosts.append(Ghost(id=f"g{i+1}", x=sp.get("x", 0), y=sp.get("y", 0)))
        self.tick_count = 0
        self.paused = False
        self.mode = "playing"
        self.consumed_pellets = 0
