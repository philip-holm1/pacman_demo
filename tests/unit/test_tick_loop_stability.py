import time

from pacman.game import FixedTimestepLoop
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.game_state import GameState
from pacman import config


def test_tick_loop_stability_basic_rate():
    """T083: Verify the fixed timestep loop produces roughly the target ticks/sec.

    We run a bounded loop (max_ticks) and measure wall-clock elapsed. The achieved
    ticks per second should be within a tolerance band of the configured target.
    A generous tolerance accounts for CI/environment noise while still catching
    large timing regressions.
    """
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    loop = FixedTimestepLoop(gs, target_fps=config.TICKS_PER_SECOND)

    target_ticks = config.TICKS_PER_SECOND * 4  # run ~4 seconds worth of ticks
    start = time.perf_counter()
    loop.start(max_ticks=target_ticks)
    elapsed = time.perf_counter() - start

    achieved_tps = gs.tick_count / elapsed if elapsed > 0 else 0
    # Allow ±25% tolerance to accommodate slow test runners
    lower = config.TICKS_PER_SECOND * 0.75
    upper = config.TICKS_PER_SECOND * 1.25
    assert gs.tick_count == target_ticks, "Tick loop did not advance expected number of ticks"
    assert lower <= achieved_tps <= upper, (
        f"Achieved TPS {achieved_tps:.2f} outside tolerance [{lower:.2f}, {upper:.2f}] for target {config.TICKS_PER_SECOND}"
    )
