from .game_state import GameState

def update_ghosts(gs: GameState) -> None:
    """Advance ghost positions one step respecting walls and frozen state.
    Deterministic: ghosts evaluate direction with priority order (right,left,down,up).
    Skips movement if game paused or not in playing mode.
    """
    if gs.paused or gs.mode != "playing":
        return
    for g in gs.ghosts:
        g.step(gs.level)
