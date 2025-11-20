from src.pacman.systems.game_state import GameState
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.scoring import apply_pellet_score

def test_feedback_visual_on_score_change():
    lvl = load_level("levels/level1.json")
    gs = GameState(level=lvl, player=Player(), level_source_path="levels/level1.json")
    assert len(gs.floating_feedback) == 0
    apply_pellet_score(gs)
    assert len(gs.floating_feedback) == 1
    assert "+" in gs.floating_feedback[0]["text"]
