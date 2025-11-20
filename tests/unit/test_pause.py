from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.game_state import GameState

def test_pause_stops_tick_increment():
    level = load_level("levels/level1.json")
    gs = GameState(level=level, player=Player())
    gs.tick(); gs.tick(); assert gs.tick_count == 2
    gs.toggle_pause()
    gs.tick(); gs.tick(); assert gs.tick_count == 2  # paused
    gs.toggle_pause()
    gs.tick(); assert gs.tick_count == 3
