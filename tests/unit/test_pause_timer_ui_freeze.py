from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.powerup_manager import powerup_manager
from src.pacman.systems.hud_powerups import render_powerup_hud_stub
from src.pacman import config

def test_pause_freezes_display_remaining():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
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
