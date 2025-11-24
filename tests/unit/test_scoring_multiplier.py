from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager
from pacman.systems.scoring import apply_pellet_score
from pacman import config

def test_scoring_multiplier_math():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    # Collect two multiplier powerups
    gs._force_multiplier = True
    for _ in range(2):
        gs.level.spawned_powerups.append({"x": gs.player.x, "y": gs.player.y, "type": "ScoreMultiplier"})
        powerup_manager.collect_powerup(gs)
    powerup_manager.update_powerups(gs)
    assert gs.player.score_multiplier == 4
    apply_pellet_score(gs)
    # Base pellet 10 * 4 = 40
    assert gs.player.score == 40
