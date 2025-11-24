from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager

def test_ghost_freeze_no_score_change():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs._force_type = "GhostFreeze"
    gs.level.spawned_powerups.append({"x": gs.player.x, "y": gs.player.y, "type": "GhostFreeze"})
    before = gs.player.score
    powerup_manager.collect_powerup(gs)
    powerup_manager.update_powerups(gs)
    assert gs.player.score == before
