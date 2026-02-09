# Skin Contract

## Config Schema (YAML/JSON)

```json
{
  "skin": {
    "selected": "default",
    "available": [
      {
        "name": "default",
        "display_name": "Default",
        "assets": {
          "player_sprite": "assets/sprites/player.png",
          "ghost_sprite": "assets/sprites/ghost.png",
          "powerup_sprite": "assets/sprites/powerup.png",
          "pellet_sprite": "assets/sprites/pellet.png"
        }
      },
      {
        "name": "green_star",
        "display_name": "Green Star",
        "assets": {
          "player_sprite": "assets/sprites/skins/green_star/player.png",
          "ghost_sprite": "assets/sprites/skins/green_star/ghost.png",
          "powerup_sprite": "assets/sprites/skins/green_star/powerup.png",
          "pellet_sprite": "assets/sprites/skins/green_star/pellet.png"
        },
        "metadata": {
          "base_tile_px": 64,
          "scales": [1,2]
        }
      }
    ]
  }
}
```

## Runtime Contract
- Renderer reads selected skin from settings and loads corresponding assets.
- On asset load failure: log warning and fall back to default asset for that category.
- No changes to collision boxes or timing.
