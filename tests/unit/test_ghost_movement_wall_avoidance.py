from pacman.entities.ghost import Ghost
from pacman.levels.loader import Level
from pacman.systems.game_state import GameState
from pacman.systems.ghost_ai import update_ghosts


def test_ghost_movement_respects_walls():
    # Simple corridor with wall barrier on right side
    grid = [
        "#####",
        "#...#",
        "#####",
    ]
    lvl = Level(
        id="test",
        width=5,
        height=3,
        tile_grid=grid,
        pellet_positions=[],
        ghost_spawn_points=[],
        player_spawn={"x": 1, "y": 1},
    )
    g = Ghost(id="g1", x=1, y=1)
    gs = GameState(level=lvl, player=None)  # type: ignore
    gs.ghosts.append(g)
    # Run several updates; ghost should move right until wall then choose new valid direction (down or up blocked, left allowed)
    for _ in range(15):
        update_ghosts(gs)
        assert not lvl.is_wall(g.x, g.y)
    # Force frozen state and ensure position stops changing
    g.state = "frozen"
    frozen_x, frozen_y = g.x, g.y
    for _ in range(5):
        update_ghosts(gs)
    assert (g.x, g.y) == (frozen_x, frozen_y)
