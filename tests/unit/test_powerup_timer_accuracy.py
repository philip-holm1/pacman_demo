from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager
from pacman.systems.hud_powerups import render_powerup_hud_stub
from pacman import config

def test_timer_accuracy_within_half_second():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs.level.spawned_powerups.append({"x": gs.player.x, "y": gs.player.y, "type": "SpeedBoost"})
    inst = powerup_manager.collect_powerup(gs)
    assert inst is not None
    # Advance half duration
    half = inst.expires_at_tick - (inst.expires_at_tick - inst.start_tick)//2
    gs.tick_count = half
    display = render_powerup_hud_stub(gs)
    remaining_display = display[0]["remaining_seconds"]
    true_remaining = (inst.expires_at_tick - gs.tick_count) / config.TICKS_PER_SECOND
    assert abs(remaining_display - true_remaining) <= 0.5
