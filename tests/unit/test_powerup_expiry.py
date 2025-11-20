from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.powerup_manager import powerup_manager
from src.pacman import config

def test_powerup_expiry_removes_instance():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
    inst = powerup_manager.collect_powerup(gs)
    assert inst is not None
    # Fast-forward to just before expiry
    gs.tick_count = inst.expires_at_tick - 1
    powerup_manager.update_powerups(gs)
    assert len(gs.player.active_powerups) == 1
    # Advance to expiry tick
    gs.tick_count = inst.expires_at_tick
    powerup_manager.update_powerups(gs)
    assert len(gs.player.active_powerups) == 0
