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
        # random direction occasionally
        if random.random() < 0.2:
            dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1),(0,0)])
        else:
            dx, dy = 0, 0
        return InputSample(move_dx=dx, move_dy=dy)

def main(duration_seconds: int = 300):
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn['x'], y=level.player_spawn['y'])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    loop = FixedTimestepLoop(gs, input_handler=RandomInput())
    end_tick = duration_seconds * 60
    while gs.tick_count < end_tick and loop.running:
        loop.tick_logic()
    print(f"Smoke playtest complete ticks={gs.tick_count} score={gs.player.score}")

if __name__ == "__main__":
    main()
