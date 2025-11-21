from src.pacman.levels.loader import Level
from src.pacman.entities.player import Player
from src.pacman.systems.game_state import GameState
from src.pacman.game import FixedTimestepLoop


class DummyInput:
    def __init__(self, move_dx=1, move_dy=0):
        self._move_dx = move_dx
        self._move_dy = move_dy
        self.available = False

    def poll(self):  # mimic InputHandler.poll
        from src.pacman.systems.input import InputSample
        return InputSample(move_dx=self._move_dx, move_dy=self._move_dy)


def test_game_over_freezes_player_and_blocks_scoring():
    # Minimal level with open space
    lvl = Level(
        id="t",
        width=5,
        height=5,
        tile_grid=["#####","#...#","#...#","#...#","#####"],
        pellet_positions=[{"x":2,"y":2}],
        ghost_spawn_points=[],
        player_spawn={"x":1,"y":1},
    )
    player = Player(x=1, y=1)
    gs = GameState(level=lvl, player=player)
    gs.mode = "game_over"
    loop = FixedTimestepLoop(gs, input_handler=DummyInput())
    start_pos = (player.x, player.y)
    start_score = player.score
    # Run several ticks; movement and scoring should not change.
    for _ in range(20):
        loop.tick_logic()
    assert (player.x, player.y) == start_pos, "Player moved during game_over state"
    assert player.score == start_score, "Score changed during game_over state"
