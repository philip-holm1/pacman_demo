from pacman.systems.powerup_manager import powerup_manager
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.game_state import GameState
from pacman import config


def test_powerup_empty_tile_spawn_invariant():
    """T084: Powerup spawns only on an empty floor tile (not a pellet tile)."""
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")

    # Remove some pellets to create empty floor tiles for powerup spawn
    # (simulating pellets being consumed during gameplay)
    for _ in range(config.POWERUP_PELLET_THRESHOLD):
        if gs.level.pellet_positions:
            gs.level.pellet_positions.pop(0)
    # Get current pellet set after removal (these are the remaining pellets)
    current_pellet_set = {(p["x"], p["y"]) for p in gs.level.pellet_positions}
    # Trigger spawn by setting consumed pellets threshold
    gs.consumed_pellets = config.POWERUP_PELLET_THRESHOLD
    powerup_manager.update_powerups(gs)

    # Check spawned_powerups list instead of pellet_positions
    spawned_powerups = gs.level.spawned_powerups
    assert spawned_powerups, "Expected a powerup spawn but found none"
    # Expect exactly one spawn for this threshold condition
    assert len(spawned_powerups) == 1, f"Expected single spawned powerup, got {len(spawned_powerups)}"
    powerup = spawned_powerups[0]
    sx, sy = powerup["x"], powerup["y"]
    # Invariant checks: powerup should NOT overlap current pellet positions
    assert (sx, sy) not in current_pellet_set, "Spawn overlapped an existing pellet tile"
    assert not level.is_wall(sx, sy), "Spawn placed on a wall tile"
