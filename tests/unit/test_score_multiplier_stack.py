from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.powerup_manager import powerup_manager
from src.pacman import config

def test_score_multiplier_stacking():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    # Force multiplier stacking deterministically
    gs._force_multiplier = True
    for _ in range(2):
        gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
        powerup_manager.collect_powerup(gs)
    powerup_manager.update_powerups(gs)
    assert gs.player.score_multiplier == 4
