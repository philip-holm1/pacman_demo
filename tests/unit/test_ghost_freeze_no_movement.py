from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.entities.ghost import Ghost
from src.pacman.systems.powerup_manager import powerup_manager

def test_ghost_freeze_prevents_position_change():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    gs.ghosts.append(Ghost(id="g1", x=2, y=2))
    gs._force_type = "GhostFreeze"
    gs.level.pellet_positions.append({"x": gs.player.x, "y": gs.player.y})
    powerup_manager.collect_powerup(gs)
    powerup_manager.update_powerups(gs)
    # Simulate would-be ghost movement attempt (ignored if frozen)
    for g in gs.ghosts:
        if g.state != "frozen":
            g.x += 1
    assert gs.ghosts[0].x == 2
