from ..systems.game_state import GameState


def evaluate_state(gs: GameState) -> None:
    if gs.player.lives <= 0:
        gs.mode = "game_over"
        return
    if len(gs.level.pellet_positions) == 0:
        gs.mode = "victory"
        return
    gs.mode = "playing"


def handle_restart(gs: GameState) -> None:
    gs.restart()
