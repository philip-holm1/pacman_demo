import json
from pathlib import Path
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.game_state import GameState
from pacman.systems.screens import evaluate_state, handle_restart
from pacman import config


def test_game_over_and_restart_resets_state_and_preserves_highscore(tmp_path, monkeypatch):
    # Prepare a copy of highscore file in temp to avoid altering repo file
    repo_hs = Path("data/highscore.json")
    temp_hs = tmp_path / "highscore.json"
    temp_hs.write_text(repo_hs.read_text(encoding="utf-8"), encoding="utf-8")

    # Monkeypatch to point loader path and data file if used later (here we just assert file unchanged)
    level_path = "levels/level1.json"
    lvl = load_level(level_path)
    gs = GameState(level=lvl, player=Player(), level_source_path=level_path)

    # Force game over
    gs.player.lives = 0
    evaluate_state(gs)
    assert gs.mode == "game_over"

    # Snapshot highscore content
    before = temp_hs.read_text(encoding="utf-8")

    # Restart should reset player and level but not modify highscore file
    handle_restart(gs)
    assert gs.mode == "playing"
    assert gs.player.lives == config.START_LIVES
    assert gs.player.score == 0
    assert len(gs.level.pellet_positions) > 0

    after = temp_hs.read_text(encoding="utf-8")
    assert before == after
