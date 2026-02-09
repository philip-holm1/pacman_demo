TICKS_PER_SECOND = 60
DEFAULT_POWERUP_DURATION = 8.0
START_LIVES = 3
# Spec uses POWERUP_PELLET_INTERVAL terminology; retain old name for compatibility
POWERUP_PELLET_THRESHOLD = 30  # spawn attempt every N pellets consumed
POWERUP_PELLET_INTERVAL = POWERUP_PELLET_THRESHOLD
MAX_SCORE_MULTIPLIER = 8
BASE_PLAYER_MOVE_INTERVAL_TICKS = 8  # player moves every 8 ticks (~7.5 tiles/sec baseline)
GHOST_MOVE_INTERVAL_TICKS = 10  # ghosts move every 10 ticks (~6 tiles/sec - slower than player for escapeability)
GHOST_DECISION_INTERVAL_TICKS = 5  # deprecated - now decisions made at intersections
FRIGHTENED_EXTENSION_TICKS = 180  # 3 seconds
SCATTER_DURATION_TICKS = 420  # 7 seconds
CHASE_DURATION_TICKS = 1200  # 20 seconds

# Skin configuration
SELECTED_SKIN = "default"  # Can be "default" or "green_star"

AVAILABLE_SKINS = {
    "default": {
        "name": "default",
        "display_name": "Default",
        "assets": {
            "player_sprite": None,  # None means use procedural rendering
            "ghost_sprite": None,
            "powerup_sprite": None,
            "pellet_sprite": None,
        }
    },
    "green_star": {
        "name": "green_star",
        "display_name": "Green Star",
        "assets": {
            "player_sprite": "assets/sprites/skins/green_star/player.png",
            "ghost_sprite": "assets/sprites/skins/green_star/ghost.png",
            "powerup_sprite": "assets/sprites/skins/green_star/powerup.png",
            "pellet_sprite": "assets/sprites/skins/green_star/pellet.png",
        },
        "metadata": {
            "base_tile_px": 64,
            "scales": [1, 2]
        }
    }
}

def load_skin_preference() -> str:
    """Load the selected skin from settings.json.
    
    Returns:
        The selected skin name, defaulting to "default" if not found.
    """
    import json
    import os
    settings_path = "data/settings.json"
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
                skin = settings.get("skin", {}).get("selected", "default")
                if skin in AVAILABLE_SKINS:
                    return skin
        except (json.JSONDecodeError, IOError):
            pass
    return "default"

def save_skin_preference(skin_name: str) -> None:
    """Save the selected skin to settings.json.
    
    Args:
        skin_name: The name of the skin to save (must be in AVAILABLE_SKINS).
    """
    import json
    import os
    from datetime import datetime
    
    if skin_name not in AVAILABLE_SKINS:
        skin_name = "default"
    
    settings_path = "data/settings.json"
    settings = {}
    
    # Load existing settings if file exists
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, IOError):
            settings = {}
    
    # Update skin preference
    settings["skin"] = {
        "selected": skin_name,
        "updated_at": datetime.now().isoformat()
    }
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
