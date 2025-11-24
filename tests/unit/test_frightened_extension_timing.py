from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.ghost_ai import trigger_frightened, tick_modes
from pacman import config


def advance(gs: GameState, ticks: int) -> None:
    for _ in range(ticks):
        gs.tick()
        tick_modes(gs)


def test_frightened_extension_adds_duration():
    """T087: Verify invoking frightened again extends remaining duration by FRIGHTENED_EXTENSION_TICKS."""
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    assert gs.frightened_ticks_remaining == 0

    # Initial trigger
    trigger_frightened(gs)
    assert gs.frightened_ticks_remaining == config.FRIGHTENED_EXTENSION_TICKS
    initial_remaining = gs.frightened_ticks_remaining

    # Advance some ticks, then trigger again for extension
    advance(gs, initial_remaining // 3)  # consume ~1/3
    remaining_before_extension = gs.frightened_ticks_remaining
    trigger_frightened(gs)  # extend
    expected = remaining_before_extension + config.FRIGHTENED_EXTENSION_TICKS
    assert gs.frightened_ticks_remaining == expected, (
        f"Expected frightened remaining {expected} after extension, got {gs.frightened_ticks_remaining}"
    )

    # Advance full remaining to ensure it ultimately reaches zero
    advance(gs, gs.frightened_ticks_remaining)
    assert gs.frightened_ticks_remaining == 0, "Frightened duration should expire to zero"
    # Underlying cycle restored (mode not frightened)
    assert gs.ghost_cycle_mode != "frightened"
