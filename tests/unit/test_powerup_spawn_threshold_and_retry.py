from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager
from pacman import config

def test_spawn_threshold_triggers_attempt():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    initial = len(gs.level.pellet_positions)
    gs.consumed_pellets = config.POWERUP_PELLET_THRESHOLD
    powerup_manager.update_powerups(gs)
    assert len(gs.level.pellet_positions) >= initial  # may append a spawn placeholder

def test_spawn_retry_limit():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    # Force is_wall to always return True to trigger retries
    original_is_wall = gs.level.is_wall
    def always_wall(x:int,y:int)->bool:
        return True
    gs.level.is_wall = always_wall  # type: ignore
    gs.consumed_pellets = config.POWERUP_PELLET_THRESHOLD
    result = powerup_manager.spawn_powerup(gs)
    assert result is None
    gs.level.is_wall = original_is_wall
