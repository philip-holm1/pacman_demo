from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.powerup_manager import powerup_manager
from src.pacman import config

def test_invincibility_blink_toggles_interval():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs._force_type = "InvincibilityBlink"
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
    inst = powerup_manager.collect_powerup(gs)
    interval_ticks = max(1, int(0.2 * config.TICKS_PER_SECOND))
    initial_state = gs.player.blink_on
    # Advance to next toggle boundary
    gs.tick_count = interval_ticks
    powerup_manager.update_powerups(gs)
    assert gs.player.blink_on != initial_state
