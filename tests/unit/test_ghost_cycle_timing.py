from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.ghost_ai import tick_modes, trigger_frightened
from pacman import config


def advance(gs: GameState, ticks: int) -> None:
    for _ in range(ticks):
        gs.tick()
        tick_modes(gs)


def test_ghost_cycle_timing_with_frightened_pause():
    """T096: Verify scatter/chase durations and pause/resume semantics during frightened."""
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")

    # Advance to end of first scatter; expect switch to chase
    advance(gs, config.SCATTER_DURATION_TICKS)
    assert gs.ghost_cycle_mode == "chase"
    assert gs.ghost_cycle_ticks == 0

    # Advance partially into chase then trigger frightened
    advance(gs, 200)
    pre_ticks = gs.ghost_cycle_ticks
    trigger_frightened(gs)
    assert gs.ghost_cycle_mode == "frightened"
    # During frightened, underlying cycle ticks freeze
    advance(gs, config.FRIGHTENED_EXTENSION_TICKS // 2)
    assert gs.ghost_cycle_ticks == pre_ticks

    # Finish frightened
    advance(gs, config.FRIGHTENED_EXTENSION_TICKS - (config.FRIGHTENED_EXTENSION_TICKS // 2))
    assert gs.frightened_ticks_remaining == 0
    # Resume chase mode with same tick count
    assert gs.ghost_cycle_mode == "chase"
    assert gs.ghost_cycle_ticks == pre_ticks

    # Advance remaining chase duration to cycle back to scatter
    remaining = config.CHASE_DURATION_TICKS - pre_ticks
    advance(gs, remaining)
    assert gs.ghost_cycle_mode == "scatter"
    assert gs.ghost_cycle_ticks == 0
