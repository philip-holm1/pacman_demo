import time
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.game_state import GameState
from src.pacman.game import FixedTimestepLoop
from src.pacman.systems.perf import PerfTracker
from src.pacman import config

class NullInput:
    def __init__(self):
        self.available = False
    def poll(self):
        from src.pacman.systems.input import InputSample
        return InputSample()

def run_capture(ticks: int = 600):
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn['x'], y=level.player_spawn['y'])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    loop = FixedTimestepLoop(gs, input_handler=NullInput())
    perf = PerfTracker()
    last = time.perf_counter()
    while gs.tick_count < ticks and loop.running:
        now = time.perf_counter()
        frame = now - last
        last = now
        perf.record_frame(frame)
        loop.tick_logic()
    return perf

if __name__ == "__main__":
    perf = run_capture()
    avg_fps = perf.avg_fps()
    worst_ms = perf.worst_ms()
    print(f"Avg FPS: {avg_fps:.2f}\nWorst Frame (ms): {worst_ms:.2f}")
    if avg_fps < 30 or worst_ms > 120:
        raise SystemExit("Performance thresholds not met")
