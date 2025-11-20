from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.powerup_manager import powerup_manager
from src.pacman import config

def test_powerup_duration_refresh():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    # Simulate spawn then collect SpeedBoost twice refreshing
    inst1 = powerup_manager.definitions["SpeedBoost"]
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
    coll1 = powerup_manager.collect_powerup(gs)
    assert coll1 is not None and coll1.type == "SpeedBoost"
    first_expiry = coll1.expires_at_tick
    # Advance some ticks then collect again to refresh expiry
    gs.tick_count += config.TICKS_PER_SECOND // 2
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
    coll2 = powerup_manager.collect_powerup(gs)
    # Find existing refreshed instance
    refreshed = [p for p in gs.player.active_powerups if p.type == "SpeedBoost"][0]
    assert refreshed.expires_at_tick > first_expiry
