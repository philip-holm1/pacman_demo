# Quickstart — Enable Green Star Skin

## Usage

1. Start the game by running `python -m pacman` (with PYTHONPATH set to `src/`)
2. During gameplay, press the **S** key to toggle between available skins
3. The current skin name is displayed at the bottom of the screen
4. Your skin selection is automatically saved to `data/settings.json`
5. The selected skin will be loaded automatically the next time you start the game

## Available Skins

- **Default**: Standard procedural rendering (circles for player/pellets, squares for ghosts)
- **Green Star**: Themed sprite-based rendering (requires assets in `assets/sprites/skins/green_star/`)

## Notes

- Skin selection persists across game restarts via `data/settings.json`
- If a themed asset fails to load, the game automatically falls back to default procedural rendering for that category
- Skins are purely visual - gameplay mechanics, collision detection, and timing remain unchanged
- Press **S** at any time during gameplay to cycle through available skins
- Press **P** to pause, **R** to restart after game over/victory, **ESC** to quit

## Implementation Details

The skin system supports:
- Sprite-based rendering for player, ghosts, powerups, and pellets
- Automatic fallback to procedural rendering if assets are missing
- Visual effects compatibility (invincibility glow, frozen ghost overlays)
- Zero impact on gameplay logic and performance
