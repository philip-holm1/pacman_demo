import time, random
from src.pacman.levels.loader import load_level
from src.pacman.entities.player import Player
from src.pacman.systems.game_state import GameState
from src.pacman.game import FixedTimestepLoop

class RandomInput:
    def __init__(self):
        self.available = False
    def poll(self):
        from src.pacman.systems.input import InputSample
        dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1),(0,0)])
        return InputSample(move_dx=dx, move_dy=dy)

def main(minutes: int = 60):
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn['x'], y=level.player_spawn['y'])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    loop = FixedTimestepLoop(gs, input_handler=RandomInput())
    target_ticks = minutes * 60 * 60
    start = time.perf_counter()
    while gs.tick_count < target_ticks and loop.running:
        loop.tick_logic()
    elapsed = time.perf_counter() - start
    print(f"Stability test complete minutes={elapsed/60:.2f} ticks={gs.tick_count} score={gs.player.score}")

if __name__ == "__main__":
    main()
