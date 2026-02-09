from pacman.systems.game_state import GameState
from pacman.levels.loader import load_level
from pacman.entities.player import Player
from pacman.systems.powerup_manager import PowerupManager

class DummyLevel:
    def __init__(self):
        self.width = 5
        self.height = 5
        self.tile_grid = ["#####","#...#","#...#","#...#","#####"]
        self.pellet_positions = []
        self.ghost_spawn_points = []
    def is_wall(self, x:int,y:int)->bool:
        return True  # Force wall everywhere so spawn fails

def test_overlap_avoidance_retry_skip():
    lvl = DummyLevel()
    gs = GameState(level=lvl, player=Player(), level_source_path=None)
    pm = PowerupManager()
    pm.spawn_retry_limit = 3
    result = pm.spawn_powerup(gs)
    assert result is None  # After retries returns None without exception
