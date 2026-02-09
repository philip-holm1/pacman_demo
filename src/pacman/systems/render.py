from typing import Any, Optional, Dict
from .game_state import GameState
from .perf import PerfTracker
from .. import config
import os

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

# Cache for loaded skin sprites
_skin_sprite_cache: Dict[str, Any] = {}

def load_skin_assets(gs: GameState, pygame: Any) -> Dict[str, Any]:
    """Load skin assets for the selected skin with fallback to default procedural rendering.
    
    Args:
        gs: GameState containing selected_skin
        pygame: Pygame module for loading images
        
    Returns:
        Dictionary with asset keys mapped to loaded pygame surfaces or None for procedural rendering
    """
    skin_name = gs.selected_skin
    cache_key = f"{skin_name}"
    
    # Return cached assets if available
    if cache_key in _skin_sprite_cache:
        return _skin_sprite_cache[cache_key]
    
    assets = {
        "player_sprite": None,
        "ghost_sprite": None,
        "powerup_sprite": None,
        "pellet_sprite": None,
    }
    
    # Get skin configuration
    skin_config = config.AVAILABLE_SKINS.get(skin_name, config.AVAILABLE_SKINS["default"])
    skin_assets = skin_config.get("assets", {})
    
    # Try to load each asset, fall back to None (procedural) on failure
    for asset_key, asset_path in skin_assets.items():
        if asset_path is None:
            continue
        
        if os.path.exists(asset_path):
            try:
                surface = pygame.image.load(asset_path).convert_alpha()
                assets[asset_key] = surface
            except Exception as e:
                print(f"[render] Warning: Failed to load {asset_path}: {e}. Using default rendering.")
                assets[asset_key] = None
        else:
            print(f"[render] Warning: Asset not found at {asset_path}. Using default rendering.")
            assets[asset_key] = None
    
    # Cache the loaded assets
    _skin_sprite_cache[cache_key] = assets
    return assets


def render(gs: GameState, screen: Any, pygame: Any, perf: Optional[PerfTracker] = None) -> None:
    screen.fill(COLORS["bg"])
    
    # Load skin assets
    skin_assets = load_skin_assets(gs, pygame)
    
    # Use green tint for Green Star skin when assets are missing (temporary visual indicator)
    is_green_star = gs.selected_skin == "green_star"
    
    # Walls & floor
    for y, row in enumerate(gs.level.tile_grid):
        for x, ch in enumerate(row):
            if ch == "#":
                wall_color = (20, 80, 40) if is_green_star else COLORS["wall"]
                pygame.draw.rect(screen, wall_color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Pellets - use sprite if available, otherwise procedural
    pellet_sprite = skin_assets.get("pellet_sprite")
    for p in gs.level.pellet_positions:
        cx = p["x"] * TILE_SIZE + TILE_SIZE // 2
        cy = p["y"] * TILE_SIZE + TILE_SIZE // 2
        if pellet_sprite:
            # Scale sprite to fit tile and blit
            scaled = pygame.transform.scale(pellet_sprite, (TILE_SIZE // 3, TILE_SIZE // 3))
            rect = scaled.get_rect(center=(cx, cy))
            screen.blit(scaled, rect)
        else:
            pellet_color = (100, 255, 150) if is_green_star else COLORS["pellet"]
            pygame.draw.circle(screen, pellet_color, (cx, cy), TILE_SIZE // 6)
    # Powerups - use sprite if available, otherwise procedural based on type
    powerup_sprite = skin_assets.get("powerup_sprite")
    for p in gs.level.spawned_powerups:
        cx = p["x"] * TILE_SIZE + TILE_SIZE // 2
        cy = p["y"] * TILE_SIZE + TILE_SIZE // 2
        powerup_type = p.get("type", "SpeedBoost")
        
        if powerup_sprite:
            # Use skin sprite for all powerup types
            scaled = pygame.transform.scale(powerup_sprite, (TILE_SIZE // 2, TILE_SIZE // 2))
            rect = scaled.get_rect(center=(cx, cy))
            screen.blit(scaled, rect)
        else:
            # Procedural rendering (default)
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
    # Player - use sprite if available, otherwise procedural (with invincibility blink effect)
    player_sprite = skin_assets.get("player_sprite")
    if gs.player.blink_on:
        cx = gs.player.x * TILE_SIZE + TILE_SIZE // 2
        cy = gs.player.y * TILE_SIZE + TILE_SIZE // 2
        has_invincibility = any(p.type == "InvincibilityBlink" for p in gs.player.active_powerups)
        
        if player_sprite:
            # Use skin sprite
            if has_invincibility:
                # Draw outer glow
                pygame.draw.circle(screen, (255, 0, 255), (cx, cy), TILE_SIZE // 2 - 2)
            scaled = pygame.transform.scale(player_sprite, (TILE_SIZE - 8, TILE_SIZE - 8))
            rect = scaled.get_rect(center=(cx, cy))
            screen.blit(scaled, rect)
        else:
            # Procedural rendering (default)
            player_color = (100, 255, 100) if is_green_star else COLORS["player"]
            if has_invincibility:
                # Draw outer glow
                glow_color = (150, 255, 150) if is_green_star else (255, 0, 255)
                pygame.draw.circle(screen, glow_color, (cx, cy), TILE_SIZE // 2 - 2)
            pygame.draw.circle(screen, player_color, (cx, cy), TILE_SIZE // 2 - 4)
            # Draw star shape for green_star skin
            if is_green_star:
                import math
                points = []
                for i in range(5):
                    angle = (math.pi * 2 * i / 5) - math.pi / 2
                    px = cx + (TILE_SIZE // 2 - 6) * math.cos(angle)
                    py = cy + (TILE_SIZE // 2 - 6) * math.sin(angle)
                    points.append((px, py))
                pygame.draw.polygon(screen, (50, 200, 50), points, 2)
    # Ghosts - use sprite if available, otherwise procedural (with frozen state visual)
    ghost_sprite = skin_assets.get("ghost_sprite")
    for g in gs.ghosts:
        gx = g.x * TILE_SIZE + 4
        gy = g.y * TILE_SIZE + 4
        
        if ghost_sprite:
            # Use skin sprite
            scaled = pygame.transform.scale(ghost_sprite, (TILE_SIZE - 8, TILE_SIZE - 8))
            screen.blit(scaled, (gx, gy))
            # Add ice effect for frozen ghosts
            if g.state == "frozen":
                pygame.draw.rect(screen, (200, 230, 255), (gx, gy, TILE_SIZE - 8, TILE_SIZE - 8), 2)
        else:
            # Procedural rendering (default)
            ghost_color = (100, 255, 150) if is_green_star else COLORS["ghost"]
            if g.state == "frozen":
                ghost_color = (100, 150, 255)  # Light blue for frozen ghosts
            pygame.draw.rect(screen, ghost_color, (gx, gy, TILE_SIZE - 8, TILE_SIZE - 8))
            # Add ice effect for frozen ghosts
            if g.state == "frozen":
                pygame.draw.rect(screen, (200, 230, 255), (gx, gy, TILE_SIZE - 8, TILE_SIZE - 8), 2)
    # Mode overlay (simple text)
    font = pygame.font.SysFont(None, 24)
    if gs.mode == "playing":
        fps_info = ""
        if perf is not None:
            fps_info = f" FPS:{perf.avg_fps():.1f} Worst:{perf.worst_ms():.1f}ms"
        skin_name = config.AVAILABLE_SKINS.get(gs.selected_skin, {}).get("display_name", "Unknown")
        status = f"Mode:{gs.mode} L:{gs.player.lives} S:{gs.player.score} HS:{gs.high_score} Mult:{gs.player.score_multiplier}{fps_info}"
        txt = font.render(status, True, (255, 255, 255))
        screen.blit(txt, (8, 8))
        
        # Display current skin (press S to change)
        skin_txt = font.render(f"Skin: {skin_name} (Press S to change)", True, (180, 180, 180))
        screen.blit(skin_txt, (8, screen.get_height() - 30))
        
        # Display active powerups
        if gs.player.active_powerups:
            y_offset = 32
            powerup_label = font.render("Active Powerups:", True, (255, 255, 100))
            screen.blit(powerup_label, (8, y_offset))
            y_offset += 20
            
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
