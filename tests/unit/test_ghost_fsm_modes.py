from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.ghost_ai import tick_modes, trigger_frightened
from pacman import config


def advance_ticks(gs: GameState, ticks: int) -> None:
    for _ in range(ticks):
        gs.tick()
        tick_modes(gs)


def test_ghost_fsm_modes_transitions_and_frightened_restore():
    """T085: Verify ghost FSM cycles scatter→chase→scatter and frightened override/restore semantics.

    Expectations:
    1. Start in scatter.
    2. After SCATTER_DURATION_TICKS ticks -> mode switches to chase, cycle tick counter resets.
    3. After CHASE_DURATION_TICKS ticks in chase -> mode switches back to scatter, counter resets.
    4. Trigger frightened mid-scatter: mode becomes frightened; underlying cycle mode & ticks snapshot preserved.
    5. During frightened, cycle ticks do not advance.
    6. After frightened duration expires, restore underlying mode & ticks snapshot; cycle resumes from stored tick count.
    """
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")

    # 1. Initial state
    assert gs.ghost_cycle_mode == "scatter"
    assert gs.ghost_cycle_ticks == 0

    # 2. Advance through scatter duration
    advance_ticks(gs, config.SCATTER_DURATION_TICKS)
    assert gs.ghost_cycle_mode == "chase"
    assert gs.ghost_cycle_ticks == 0, "Cycle ticks should reset on mode switch to chase"

    # 3. Advance through chase duration
    advance_ticks(gs, config.CHASE_DURATION_TICKS)
    assert gs.ghost_cycle_mode == "scatter"
    assert gs.ghost_cycle_ticks == 0, "Cycle ticks should reset on mode switch back to scatter"

    # Advance some ticks into scatter then trigger frightened
    advance_ticks(gs, 50)
    pre_fright_mode = gs.ghost_cycle_mode
    pre_fright_ticks = gs.ghost_cycle_ticks
    trigger_frightened(gs)  # default extension
    assert gs.ghost_cycle_mode == "frightened"
    assert gs.frightened_ticks_remaining == config.FRIGHTENED_EXTENSION_TICKS
    # Underlying snapshot stored
    assert gs._underlying_cycle_mode == pre_fright_mode
    assert gs._underlying_cycle_ticks_snapshot == pre_fright_ticks

    # 5. During frightened, cycle ticks should not change
    advance_ticks(gs, config.FRIGHTENED_EXTENSION_TICKS // 2)
    assert gs.ghost_cycle_mode == "frightened"
    assert gs.ghost_cycle_ticks == pre_fright_ticks, "Cycle ticks should freeze during frightened"

    # Finish frightened duration
    advance_ticks(gs, config.FRIGHTENED_EXTENSION_TICKS - (config.FRIGHTENED_EXTENSION_TICKS // 2))
    assert gs.frightened_ticks_remaining == 0
    assert gs.ghost_cycle_mode == pre_fright_mode, "Cycle mode should restore after frightened"
    assert gs.ghost_cycle_ticks == pre_fright_ticks, "Cycle ticks should restore to snapshot value"

    # 6. Ensure cycle resumes advancing from restored snapshot
    advance_ticks(gs, 25)
    assert gs.ghost_cycle_ticks == pre_fright_ticks + 25, "Cycle ticks should resume from restored value"
