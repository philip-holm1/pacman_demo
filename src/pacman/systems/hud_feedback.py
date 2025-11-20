from .game_state import GameState

def get_feedback(gs: GameState):
    return list(gs.floating_feedback)

# Purge old entries (e.g., older than N ticks) placeholder

def prune_feedback(gs: GameState, max_age_ticks: int = 180) -> None:
    gs.floating_feedback = [e for e in gs.floating_feedback if gs.tick_count - e["tick"] <= max_age_ticks]
