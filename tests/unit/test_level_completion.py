from pacman.levels.loader import Level
from pacman.entities.player import Player
from pacman.systems.game_state import GameState
from pacman.systems.screens import evaluate_state

def test_level_completion_triggers_victory():
    lvl = Level(
        id="lvl",
        width=3,
        height=3,
        tile_grid=["###","#.#","###"],
        pellet_positions=[],
        ghost_spawn_points=[],
        player_spawn={"x":1, "y":1},
    )
    gs = GameState(level=lvl, player=Player())
    evaluate_state(gs)
    assert gs.mode == "victory"
