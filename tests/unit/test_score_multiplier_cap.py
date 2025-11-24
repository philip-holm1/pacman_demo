from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager
from pacman import config

def test_score_multiplier_cap():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs._force_multiplier = True
    # Collect multiple multiplier instances to exceed cap
    for _ in range(10):
        gs.level.spawned_powerups.append({"x": gs.player.x, "y": gs.player.y, "type": "ScoreMultiplier"})
        powerup_manager.collect_powerup(gs)
    powerup_manager.update_powerups(gs)
    assert gs.player.score_multiplier == config.MAX_SCORE_MULTIPLIER
