from .game_state import GameState

BASE_PELLET_SCORE = 10
POWERUP_BONUS = 50  # placeholder bonus for powerup collection


def add_floating_text(gs: GameState, text: str) -> None:
    gs.floating_feedback.append({"text": text, "tick": gs.tick_count})


def apply_pellet_score(gs: GameState) -> None:
    delta = BASE_PELLET_SCORE * gs.player.score_multiplier
    gs.player.score += delta
    add_floating_text(gs, f"+{delta}")


def apply_powerup_bonus(gs: GameState) -> None:
    delta = POWERUP_BONUS * gs.player.score_multiplier
    gs.player.score += delta
    add_floating_text(gs, f"+{delta}P")
