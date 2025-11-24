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
    "powerup_speed": (0, 255, 255),       # Cyan for SpeedBoost
    "powerup_freeze": (100, 200, 255),    # Light blue for GhostFreeze
    "powerup_multiplier": (255, 150, 0),  # Orange for ScoreMultiplier
    "powerup_invincibility": (255, 0, 255), # Magenta for InvincibilityBlink
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
    # Powerups (render differently based on type)
    for p in gs.level.spawned_powerups:
        cx = p["x"] * TILE_SIZE + TILE_SIZE // 2
        cy = p["y"] * TILE_SIZE + TILE_SIZE // 2
        powerup_type = p.get("type", "SpeedBoost")
        if powerup_type == "SpeedBoost":
            # Draw as larger cyan circle with outline
            pygame.draw.circle(screen, COLORS["powerup_speed"], (cx, cy), TILE_SIZE // 3)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), TILE_SIZE // 3, 2)
        elif powerup_type == "GhostFreeze":
            # Draw as light blue square
            size = TILE_SIZE // 2
            pygame.draw.rect(screen, COLORS["powerup_freeze"], (cx - size//2, cy - size//2, size, size))
            pygame.draw.rect(screen, (255, 255, 255), (cx - size//2, cy - size//2, size, size), 2)
        elif powerup_type == "ScoreMultiplier":
            # Draw as orange star (diamond shape)
            size = TILE_SIZE // 2
            points = [(cx, cy - size//2), (cx + size//2, cy), (cx, cy + size//2), (cx - size//2, cy)]
            pygame.draw.polygon(screen, COLORS["powerup_multiplier"], points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        elif powerup_type == "InvincibilityBlink":
            # Draw as magenta hexagon
            import math
            size = TILE_SIZE // 3
            points = []
            for i in range(6):
                angle = math.pi / 3 * i
                px = cx + size * math.cos(angle)
                py = cy + size * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(screen, COLORS["powerup_invincibility"], points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
    # Player (with invincibility blink effect)
    if gs.player.blink_on:
        player_color = COLORS["player"]
        # Add glow effect if invincible
        has_invincibility = any(p.type == "InvincibilityBlink" for p in gs.player.active_powerups)
        if has_invincibility:
            # Draw outer glow
            pygame.draw.circle(screen, (255, 0, 255), (gs.player.x * TILE_SIZE + TILE_SIZE // 2, gs.player.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 2)
        pygame.draw.circle(screen, player_color, (gs.player.x * TILE_SIZE + TILE_SIZE // 2, gs.player.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 4)
    # Ghosts (with frozen state visual)
    for g in gs.ghosts:
        ghost_color = COLORS["ghost"]
        if g.state == "frozen":
            ghost_color = (100, 150, 255)  # Light blue for frozen ghosts
        pygame.draw.rect(screen, ghost_color, (g.x * TILE_SIZE + 4, g.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8))
        # Add ice effect for frozen ghosts
        if g.state == "frozen":
            pygame.draw.rect(screen, (200, 230, 255), (g.x * TILE_SIZE + 4, g.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8), 2)
    # Mode overlay (simple text)
    font = pygame.font.SysFont(None, 24)
    if gs.mode == "playing":
        fps_info = ""
        if perf is not None:
            fps_info = f" FPS:{perf.avg_fps():.1f} Worst:{perf.worst_ms():.1f}ms"
        status = f"Mode:{gs.mode} L:{gs.player.lives} S:{gs.player.score} HS:{gs.high_score} Mult:{gs.player.score_multiplier}{fps_info}"
        txt = font.render(status, True, (255, 255, 255))
        screen.blit(txt, (8, 8))
        
        # Display active powerups
        if gs.player.active_powerups:
            y_offset = 32
            powerup_label = font.render("Active Powerups:", True, (255, 255, 100))
            screen.blit(powerup_label, (8, y_offset))
            y_offset += 20
            
            from .. import config
            powerup_colors = {
                "SpeedBoost": COLORS["powerup_speed"],
                "GhostFreeze": COLORS["powerup_freeze"],
                "ScoreMultiplier": COLORS["powerup_multiplier"],
                "InvincibilityBlink": COLORS["powerup_invincibility"]
            }
            
            for powerup in gs.player.active_powerups:
                remaining_ticks = max(0, powerup.expires_at_tick - gs.tick_count)
                remaining_secs = remaining_ticks / config.TICKS_PER_SECOND
                color = powerup_colors.get(powerup.type, (200, 200, 200))
                powerup_txt = font.render(f"  {powerup.type}: {remaining_secs:.1f}s", True, color)
                screen.blit(powerup_txt, (8, y_offset))
                y_offset += 18
    else:
        big_font = pygame.font.SysFont(None, 48)
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        if gs.mode == "game_over":
            title = big_font.render("GAME OVER", True, (255, 80, 80))
            screen.blit(title, (center_x - title.get_width() // 2, center_y - 120))
            score_line = font.render(f"Score: {gs.player.score}", True, (255,255,255))
            hs_line = font.render(f"High Score: {gs.high_score}", True, (255,255,0))
            restart_line = font.render("Press R to Restart", True, (200,200,200))
            screen.blit(score_line, (center_x - score_line.get_width() // 2, center_y - 40))
            screen.blit(hs_line, (center_x - hs_line.get_width() // 2, center_y - 10))
            screen.blit(restart_line, (center_x - restart_line.get_width() // 2, center_y + 30))
        elif gs.mode == "victory":
            title = big_font.render("VICTORY!", True, (120, 255, 120))
            screen.blit(title, (center_x - title.get_width() // 2, center_y - 120))
            score_line = font.render(f"Score: {gs.player.score}", True, (255,255,255))
            hs_line = font.render(f"High Score: {gs.high_score}", True, (255,255,0))
            restart_line = font.render("Press R to Play Again", True, (200,200,200))
            screen.blit(score_line, (center_x - score_line.get_width() // 2, center_y - 40))
            screen.blit(hs_line, (center_x - hs_line.get_width() // 2, center_y - 10))
            screen.blit(restart_line, (center_x - restart_line.get_width() // 2, center_y + 30))
    # Floating feedback entries
    y_offset = 32
    for fb in gs.floating_feedback[-5:]:
        t = font.render(fb["text"], True, (255, 255, 0))
        screen.blit(t, (8, y_offset))
        y_offset += 16
