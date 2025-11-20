from pathlib import Path
import json
from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.scoring import apply_pellet_score
from src.pacman.systems.highscore import ensure_loaded, update_high_score

def test_highscore_persistence(tmp_path):
    lvl = load_level("levels/level1.json")
    hs_file = tmp_path / "highscore.json"
    hs_file.write_text('{"highscore": 5}', encoding="utf-8")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json", high_score_path=str(hs_file))
    ensure_loaded(gs)
    assert gs.high_score == 5
    # Increase score beyond high score
    for _ in range(1):
        apply_pellet_score(gs)  # +10
    update_high_score(gs)
    data = json.loads(hs_file.read_text(encoding="utf-8"))
    assert data["highscore"] == gs.high_score == 10
