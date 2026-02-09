import json
from pathlib import Path
from typing import Optional
from .game_state import GameState

DEFAULT_PATH = Path("data/highscore.json")

def load_high_score(path: Optional[str] = None) -> int:
    target = Path(path) if path else DEFAULT_PATH
    try:
        if target.exists():
            with target.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return int(data.get("highscore", 0))
    except Exception:
        return 0
    return 0

def save_high_score(value: int, path: Optional[str] = None) -> None:
    target = Path(path) if path else DEFAULT_PATH
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as f:
            json.dump({"highscore": int(value)}, f)
    except Exception:
        # Silently ignore write errors
        pass

def ensure_loaded(gs: GameState) -> None:
    if gs.high_score == 0:
        gs.high_score = load_high_score(gs.high_score_path)


def update_high_score(gs: GameState) -> None:
    ensure_loaded(gs)
    if gs.player.score > gs.high_score:
        gs.high_score = gs.player.score
        save_high_score(gs.high_score, gs.high_score_path)
