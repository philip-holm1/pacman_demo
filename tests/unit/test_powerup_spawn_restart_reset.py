from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import powerup_manager
from pacman import config


def test_powerup_spawn_threshold_resets_on_restart():
    """T098: Pellet counter for spawn threshold resets on level restart (victory/game over semantics)."""
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")

    # Simulate near-threshold state then restart
    gs.consumed_pellets = config.POWERUP_PELLET_THRESHOLD - 1
    gs.restart()
    assert gs.consumed_pellets == 0, "Restart did not reset consumed pellets"

    # After restart, initial powerups are spawned (4), so count them
    initial_count = len(gs.level.spawned_powerups)
    assert initial_count == 4, "Expected 4 initial powerups after restart"
    
    # Verify that powerup spawn threshold resets to the next interval
    assert powerup_manager.next_spawn_at == config.POWERUP_PELLET_THRESHOLD, "Spawn threshold should reset to initial value"
