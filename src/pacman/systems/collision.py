from typing import List
from ..entities.player import Player
from ..entities.ghost import Ghost
from ..entities.powerup import PowerupInstance
from ..levels.loader import Level
from .game_state import GameState


def attempt_player_move(player: Player, level: Level, dx: int, dy: int) -> bool:
    nx = player.x + dx
    ny = player.y + dy
    if level.is_wall(nx, ny):
        return False
    player.move(nx, ny)
    return True


def consume_pellet_if_present(player: Player, level: Level, gs: GameState | None = None) -> bool:
    for i, pos in enumerate(level.pellet_positions):
        if pos["x"] == player.x and pos["y"] == player.y:
            del level.pellet_positions[i]
            if gs is not None:
                gs.consumed_pellets += 1
            return True
    return False


def is_invincible(player: Player) -> bool:
    for inst in player.active_powerups:
        if inst.type == "InvincibilityBlink":
            return True
    return False


def ghost_collision(player: Player, ghosts: List[Ghost]) -> bool:
    return any(g.x == player.x and g.y == player.y for g in ghosts)


def apply_ghost_collision(player: Player, ghosts: List[Ghost]) -> bool:
    if is_invincible(player):
        return False
    if ghost_collision(player, ghosts):
        if player.lives > 0:
            player.lives -= 1
        return True
    return False
