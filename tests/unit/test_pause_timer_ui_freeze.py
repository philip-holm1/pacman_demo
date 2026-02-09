from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager
from pacman.systems.hud_powerups import render_powerup_hud_stub
from pacman import config

def test_pause_freezes_display_remaining():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs.level.spawned_powerups.append({"x": gs.player.x, "y": gs.player.y, "type": "SpeedBoost"})
    inst = powerup_manager.collect_powerup(gs)
    assert inst is not None
    powerup_manager.update_powerups(gs)
    first = render_powerup_hud_stub(gs)[0]["remaining_seconds"]
    gs.toggle_pause()
    # Advance ticks but paused: tick() won't increment while paused
    for _ in range(10):
        gs.tick()
    second = render_powerup_hud_stub(gs)[0]["remaining_seconds"]
    assert first == second
