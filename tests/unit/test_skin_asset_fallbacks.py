"""Test that skin asset loading falls back correctly when assets are missing."""
import os
from unittest.mock import MagicMock, patch
from pacman.systems.render import load_skin_assets
from pacman.systems.game_state import GameState
from pacman.levels.loader import Level
from pacman.entities.player import Player


def test_fallback_to_default_when_assets_missing():
    """Test that missing skin assets fall back to None (procedural rendering)."""
    # Create a minimal game state
    level = Level(
        id="test_level",
        width=10,
        height=10,
        tile_grid=[["#"] * 10 for _ in range(10)],
        pellet_positions=[],
        spawned_powerups=[],
        player_spawn={"x": 1, "y": 1},
        ghost_spawn_points=[]
    )
    player = Player(x=1, y=1)
    gs = GameState(level=level, player=player, selected_skin="green_star")
    
    # Mock pygame
    mock_pygame = MagicMock()
    
    # Test with missing assets (paths don't exist)
    assets = load_skin_assets(gs, mock_pygame)
    
    # All assets should fall back to None since files don't exist
    assert assets["player_sprite"] is None, "Missing player sprite should fall back to None"
    assert assets["ghost_sprite"] is None, "Missing ghost sprite should fall back to None"
    assert assets["powerup_sprite"] is None, "Missing powerup sprite should fall back to None"
    assert assets["pellet_sprite"] is None, "Missing pellet sprite should fall back to None"


def test_default_skin_uses_procedural_rendering():
    """Test that default skin explicitly uses None for all assets."""
    level = Level(
        id="test_level",
        width=10,
        height=10,
        tile_grid=[["#"] * 10 for _ in range(10)],
        pellet_positions=[],
        spawned_powerups=[],
        player_spawn={"x": 1, "y": 1},
        ghost_spawn_points=[]
    )
    player = Player(x=1, y=1)
    gs = GameState(level=level, player=player, selected_skin="default")
    
    # Mock pygame
    mock_pygame = MagicMock()
    
    # Default skin should have all None assets
    assets = load_skin_assets(gs, mock_pygame)
    
    assert assets["player_sprite"] is None
    assert assets["ghost_sprite"] is None
    assert assets["powerup_sprite"] is None
    assert assets["pellet_sprite"] is None


def test_asset_cache_works():
    """Test that assets are cached after first load."""
    from pacman.systems import render
    
    # Clear the cache first
    render._skin_sprite_cache.clear()
    
    level = Level(
        id="test_level",
        width=10,
        height=10,
        tile_grid=[["#"] * 10 for _ in range(10)],
        pellet_positions=[],
        spawned_powerups=[],
        player_spawn={"x": 1, "y": 1},
        ghost_spawn_points=[]
    )
    player = Player(x=1, y=1)
    gs = GameState(level=level, player=player, selected_skin="default")
    
    mock_pygame = MagicMock()
    
    # First load
    assets1 = load_skin_assets(gs, mock_pygame)
    
    # Second load should return cached version
    assets2 = load_skin_assets(gs, mock_pygame)
    
    # Should be the same object (cached)
    assert assets1 is assets2, "Assets should be cached"
    
    # Cache key should exist
    assert "default" in render._skin_sprite_cache
