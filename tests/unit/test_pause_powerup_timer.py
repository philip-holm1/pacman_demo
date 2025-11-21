from src.pacman.entities.player import Player
from src.pacman.systems.game_state import GameState
from src.pacman.entities.powerup import PowerupInstance
from src.pacman import config

def test_powerup_timer_freezes_on_pause():
    player = Player()
    gs = GameState(level=None, player=player)  # type: ignore
    start = 0
    duration_ticks = int(2 * config.TICKS_PER_SECOND)
    inst = PowerupInstance(powerup_id="SpeedBoost", type="SpeedBoost", start_tick=start, expires_at_tick=duration_ticks)
    player.active_powerups.append(inst)
    # advance some ticks
    for _ in range(30):
        gs.tick()
    remaining_before_pause = inst.expires_at_tick - gs.tick_count
    gs.toggle_pause()
    # ticks while paused should not reduce remaining (tick() does not increment)
    for _ in range(50):
        gs.tick()
    remaining_after_pause = inst.expires_at_tick - gs.tick_count
    assert remaining_before_pause == remaining_after_pause
