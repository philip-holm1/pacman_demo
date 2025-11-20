from typing import Any
from .game_state import GameState

TILE_SIZE = 32

COLORS = {
    "bg": (0, 0, 0),
    "wall": (30, 30, 120),
    "floor": (0, 0, 0),
    "pellet": (250, 250, 0),
    "player": (255, 200, 0),
    "ghost": (255, 0, 120),
}


def render(gs: GameState, screen: Any, pygame: Any) -> None:
    screen.fill(COLORS["bg"])
    # Walls & floor
    for y, row in enumerate(gs.level.tile_grid):
        for x, ch in enumerate(row):
            if ch == "#":
                pygame.draw.rect(screen, COLORS["wall"], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    # Pellets
    for p in gs.level.pellet_positions:
        cx = p["x"] * TILE_SIZE + TILE_SIZE // 2
        cy = p["y"] * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, COLORS["pellet"], (cx, cy), TILE_SIZE // 6)
    # Player
    pygame.draw.circle(screen, COLORS["player"], (gs.player.x * TILE_SIZE + TILE_SIZE // 2, gs.player.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 4)
    # Ghosts
    for g in gs.ghosts:
        pygame.draw.rect(screen, COLORS["ghost"], (g.x * TILE_SIZE + 4, g.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8))
    # Mode overlay (simple text)
    font = pygame.font.SysFont(None, 24)
    status = f"Mode: {gs.mode} Lives: {gs.player.lives} Pellets: {len(gs.level.pellet_positions)}"
    txt = font.render(status, True, (255, 255, 255))
    screen.blit(txt, (8, 8))
