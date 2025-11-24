from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.entities.ghost import Ghost
from pacman.systems.ghost_ai import update_ghosts
from pacman import config


def test_ghost_no_immediate_reversal_except_dead_end():
    """T097: Ghost should not reverse direction immediately unless forced by wall/dead-end or mode switch.

    We simulate a corridor ensuring forward progress until a wall forces a turn; then allow reversal on dead-end.
    Current implementation keeps direction if still valid; test asserts no back-and-forth jitter.
    """
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    ghost = Ghost(id="g1", x=player.x + 1, y=player.y)
    gs.ghosts.append(ghost)

    dirs = []
    steps = config.GHOST_MOVE_INTERVAL_TICKS * 40
    for _ in range(steps):
        gs.tick()
        update_ghosts(gs)
        if gs.tick_count % config.GHOST_MOVE_INTERVAL_TICKS == 0:
            dirs.append((ghost.dir_dx, ghost.dir_dy))

    # No immediate alternation pattern like [(1,0),(-1,0),(1,0),(-1,0)...]
    for a, b, c in zip(dirs, dirs[1:], dirs[2:]):
        assert not (a == (1,0) and b == (-1,0) and c == (1,0)), "Detected immediate reversal jitter pattern"
        assert not (a == (-1,0) and b == (1,0) and c == (-1,0)), "Detected immediate reversal jitter pattern"
