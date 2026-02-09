from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.entities.ghost import Ghost
from pacman.systems import ghost_ai
from pacman import config


def test_ghost_decision_cadence():
    """T086: Ghost direction decisions occur only at configured cadence intervals.

    Decision cadence is defined by GHOST_DECISION_INTERVAL_TICKS applied on move ticks.
    Since ghosts move every GHOST_MOVE_INTERVAL_TICKS, effective direction change
    frequency is GHOST_MOVE_INTERVAL_TICKS * GHOST_DECISION_INTERVAL_TICKS.
    """
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    ghost = Ghost(id="g1", x=player.x + 1, y=player.y)
    gs.ghosts.append(ghost)

    change_ticks = []
    prev_dir = (ghost.dir_dx, ghost.dir_dy)
    total_ticks = config.GHOST_MOVE_INTERVAL_TICKS * config.GHOST_DECISION_INTERVAL_TICKS * 6
    for _ in range(total_ticks):
        gs.tick()
        ghost_ai.update_ghosts(gs)
        current_dir = (ghost.dir_dx, ghost.dir_dy)
        if current_dir != prev_dir and current_dir != (0, 0):
            change_ticks.append(gs.tick_count)
            prev_dir = current_dir

    assert change_ticks, "Expected at least one direction change"
    expected_interval = config.GHOST_MOVE_INTERVAL_TICKS * config.GHOST_DECISION_INTERVAL_TICKS
    # Verify each change tick aligns on an interval boundary since first change
    first = change_ticks[0]
    for t in change_ticks[1:]:
        diff = t - first
        assert diff % expected_interval == 0, (
            f"Direction change at tick {t} not aligned to expected interval {expected_interval} from first change {first}"
        )
    # Ensure no excessive frequency (minimum interval maintained)
    for a, b in zip(change_ticks, change_ticks[1:]):
        assert (b - a) >= expected_interval, "Direction changed sooner than expected cadence"
