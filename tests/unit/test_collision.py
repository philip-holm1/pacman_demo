from src.pacman.levels.loader import Level
from src.pacman.entities.player import Player
from src.pacman.systems.collision import attempt_player_move, consume_pellet_if_present

def make_level():
    return Level(
        id="test",
        width=3,
        height=3,
        tile_grid=["###", "#.#", "###"],
        pellet_positions=[{"x": 1, "y": 1}],
        ghost_spawn_points=[],
        player_spawn={"x": 1, "y": 1},
    )

def test_wall_block_move():
    lvl = make_level()
    p = Player(x=1, y=1)
    moved = attempt_player_move(p, lvl, 1, 0)  # into wall
    assert moved is False
    assert p.x == 1 and p.y == 1

def test_pellet_consumption():
    lvl = make_level()
    p = Player(x=1, y=1)
    assert consume_pellet_if_present(p, lvl) is True
    assert lvl.pellet_positions == []
