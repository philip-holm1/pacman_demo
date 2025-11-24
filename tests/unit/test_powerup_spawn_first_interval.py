from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager
from pacman import config


def test_powerup_spawn_occurs_at_first_interval():
    """T099: First powerup spawn occurs exactly at pellet interval threshold (e.g., 30)."""
    # Reset powerup manager state to ensure clean test
    powerup_manager.next_spawn_at = config.POWERUP_PELLET_THRESHOLD
    powerup_manager._last_spawn_index = 0
    
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    
    # Clear initial powerups spawned by game initialization (4 default)
    initial_count = len(gs.level.spawned_powerups)
    gs.level.spawned_powerups.clear()

    # Remove some pellets to create spawn spaces
    for _ in range(10):
        if gs.level.pellet_positions:
            gs.level.pellet_positions.pop(0)

    # Increment pellet counter gradually below threshold
    for i in range(config.POWERUP_PELLET_THRESHOLD - 1):
        gs.consumed_pellets = i
        powerup_manager.update_powerups(gs)
        assert len(gs.level.spawned_powerups) == 0, "No spawn expected yet"

    gs.consumed_pellets = config.POWERUP_PELLET_THRESHOLD
    powerup_manager.update_powerups(gs)
    assert len(gs.level.spawned_powerups) == 1, "Expected spawn exactly at first interval threshold"
