from typing import Any, Optional
from .game_state import GameState
from .perf import PerfTracker

TILE_SIZE = 32

COLORS = {
    "bg": (0, 0, 0),
    "wall": (30, 30, 120),
    "floor": (0, 0, 0),
    "pellet": (250, 250, 0),
    "player": (255, 200, 0),
    "ghost": (255, 0, 120),
}


def render(gs: GameState, screen: Any, pygame: Any, perf: Optional[PerfTracker] = None) -> None:
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
    fps_info = ""
    if perf is not None:
        fps_info = f" FPS:{perf.avg_fps():.1f} Worst:{perf.worst_ms():.1f}ms"
    status = f"Mode:{gs.mode} L:{gs.player.lives} S:{gs.player.score} HS:{gs.high_score} Mult:{gs.player.score_multiplier}{fps_info}"
    txt = font.render(status, True, (255, 255, 255))
    screen.blit(txt, (8, 8))
    # Floating feedback entries
    y_offset = 32
    for fb in gs.floating_feedback[-5:]:
        t = font.render(fb["text"], True, (255, 255, 0))
        screen.blit(t, (8, y_offset))
        y_offset += 16
