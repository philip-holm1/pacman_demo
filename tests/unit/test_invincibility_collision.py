from pacman.entities.player import Player
from pacman.entities.ghost import Ghost
from pacman.systems.game_state import GameState
from pacman.entities.powerup import PowerupInstance
from pacman.systems.collision import apply_ghost_collision


def test_invincibility_blocks_ghost_collision():
    player = Player(x=5, y=5, lives=3)
    ghost = Ghost(id="g1", x=5, y=5)
    gs = GameState(level=None, player=player)  # type: ignore
    inst = PowerupInstance(powerup_id="InvincibilityBlink", type="InvincibilityBlink", start_tick=0, expires_at_tick=999)
    player.active_powerups.append(inst)
    collided = apply_ghost_collision(player, [ghost])
    assert collided is False
    assert player.lives == 3
