# Data Model — Skins

## Entities

### Skin
- name: string (e.g., "green_star")
- display_name: string (e.g., "Green Star")
- assets:
  - player_sprite: path (PNG spritesheet)
  - ghost_sprite: path (PNG spritesheet; includes frightened variant)
  - powerup_sprite: path (PNG)
  - pellet_sprite: path (PNG)
- metadata:
  - base_tile_px: int (64)
  - scales: [1, 2]

### SkinPreference
- selected_skin: string ("default" | "green_star")
- updated_at: ISO timestamp
- storage: file path or config key

## Relationships
- SkinPreference references Skin by name.

## Validation Rules
- selected_skin must be one of known skins.
- All asset paths must exist; else fallback to default.
- Base tile size must match configured renderer tile size.
