from pacman.levels.loader import load_level, Level
from pacman.entities.player import Player
from pacman.systems.game_state import GameState
from pacman.systems.screens import evaluate_state, handle_restart
from pacman import config

def test_restart_from_victory_and_game_over():
    level_path = "levels/level1.json"
    lvl = load_level(level_path)
    gs = GameState(level=lvl, player=Player(), level_source_path=level_path)

    # Victory path: remove all pellets
    gs.level.pellet_positions.clear()
    evaluate_state(gs)
    assert gs.mode == "victory"
    handle_restart(gs)
    assert gs.mode == "playing"
    assert len(gs.level.pellet_positions) > 0
    assert gs.player.lives == config.START_LIVES

    # Game over path: set lives to zero
    gs.player.lives = 0
    evaluate_state(gs)
    assert gs.mode == "game_over"
    handle_restart(gs)
    assert gs.mode == "playing"
    assert gs.player.lives == config.START_LIVES
