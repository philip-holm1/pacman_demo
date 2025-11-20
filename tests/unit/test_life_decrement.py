from src.pacman.entities.player import Player
from src.pacman.entities.ghost import Ghost
from src.pacman.entities.powerup import PowerupInstance
from src.pacman.systems.collision import apply_ghost_collision

def test_life_decrement_on_ghost_collision():
    player = Player(lives=3, x=1, y=1)
    ghosts = [Ghost(id="g1", x=1, y=1)]
    collided = apply_ghost_collision(player, ghosts)
    assert collided is True
    assert player.lives == 2

def test_lives_not_below_zero():
    player = Player(lives=0, x=1, y=1)
    ghosts = [Ghost(id="g1", x=1, y=1)]
    collided = apply_ghost_collision(player, ghosts)
    assert collided is True  # collision detected but no negative lives
    assert player.lives == 0

def test_invincibility_ignores_collision():
    player = Player(lives=3, x=1, y=1)
    player.active_powerups.append(PowerupInstance(powerup_id="p", type="InvincibilityBlink", start_tick=0, expires_at_tick=10))
    ghosts = [Ghost(id="g1", x=1, y=1)]
    collided = apply_ghost_collision(player, ghosts)
    assert collided is False
    assert player.lives == 3
