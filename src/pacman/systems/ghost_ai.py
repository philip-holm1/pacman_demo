from .game_state import GameState
from .. import config

def update_ghosts(gs: GameState) -> None:
    """Advance ghost positions, throttled by GHOST_MOVE_INTERVAL_TICKS.
    Deterministic direction choice; respects walls and frozen state.
    """
    if gs.paused or gs.mode != "playing":
        return
    if (gs.tick_count % config.GHOST_MOVE_INTERVAL_TICKS) != 0:
        return
    for g in gs.ghosts:
        g.step(gs.level)
