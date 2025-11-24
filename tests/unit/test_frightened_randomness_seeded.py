import random

from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.entities.ghost import Ghost
from pacman.systems.ghost_ai import trigger_frightened, update_ghosts, tick_modes
from pacman import config


def run_frightened_path(seed: int, ticks: int) -> list[tuple[int, int]]:
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    # Override RNG seed for frightened movement
    gs.frightened_rng = random.Random(seed)
    ghost = Ghost(id="g1", x=player.x + 2, y=player.y)
    gs.ghosts.append(ghost)
    trigger_frightened(gs)
    path = []
    for _ in range(ticks):
        gs.tick()
        tick_modes(gs)
        update_ghosts(gs)
        if gs.tick_count % config.GHOST_MOVE_INTERVAL_TICKS == 0:
            path.append((ghost.x, ghost.y))
    return path


def test_frightened_randomness_seeded_reproducible():
    """T088: Frightened movement path is reproducible given identical seed."""
    ticks = config.GHOST_MOVE_INTERVAL_TICKS * 40
    seq1 = run_frightened_path(999, ticks)
    seq2 = run_frightened_path(999, ticks)
    assert seq1 == seq2, "Frightened movement paths differ for identical seed"

    # Different seed should yield a divergent path (at least one differing position)
    seq3 = run_frightened_path(1000, ticks)
    assert any(a != b for a, b in zip(seq1, seq3)), "Expected differing path with different seed"
