from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.entities.powerup import PowerupInstance
from src.pacman.systems.powerup_manager import powerup_manager
from src.pacman import config

def test_speed_and_freeze_independent():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    # Force SpeedBoost
    gs._force_type = "SpeedBoost"
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
    powerup_manager.collect_powerup(gs)
    # Force GhostFreeze
    gs._force_type = "GhostFreeze"
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
    powerup_manager.collect_powerup(gs)
    powerup_manager.update_powerups(gs)
    assert gs.player.speed_multiplier == 1.5
    # All ghosts frozen; none exist so just validate no error and blink_on unaffected
    assert gs.player.blink_on is True
