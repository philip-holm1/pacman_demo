# Data Model: Random Map Generation

**Feature**: Random Map Generation and Playable Levels  
**Date**: February 9, 2026  
**Status**: Design Reference (Phase 1 Output)  
**Spec Reference**: [spec.md](spec.md) | **Tasks**: [T011, T038-T043, T052](tasks.md)

---

## Core Entities

### 1. GeneratedMap

Represents a procedurally generated game level with all required metadata and validation state.

```python
@dataclass
class GeneratedMap:
    """A procedurally generated Pac-Man map with validated playability."""
    
    # Grid & Dimensions
    grid: List[List[int]]                    # 2D array of tile types (see TileType enum)
    width: int                               # Grid width in tiles (12, 16, or 20)
    height: int                              # Grid height in tiles (12, 16, or 20)
    size_preset: Literal["small", "medium", "large"]  # S=12x12, M=16x16, L=20x20
    
    # Spawn Locations (tile coordinates)
    pacman_spawn: Tuple[int, int]            # (x, y) where Pac-Man starts
    ghost_spawns: List[Tuple[int, int]]      # [(x1, y1), (x2, y2), ...] 2-4 spawns
    powerup_spawn_points: List[Tuple[int, int]]  # Locations where powerups can appear
    
    # Pellet & Item Placement
    pellet_positions: List[Tuple[int, int]]  # All pellet tile coordinates
    pellet_count: int                        # Total pellets on map (calculated)
    
    # Configuration & Difficulty
    config: MapConfig                        # Generation parameters used
    
    # Validation State
    validated: bool                          # True if passed all playability checks
    validation_score: ValidationScore        # Detailed validation metrics
    validated_at: str                        # ISO timestamp of validation
    
    # Metadata
    theme: str                               # Name of applied theme (standard, green_star, custom)
    seed: Optional[int]                      # Optional seed for reproducibility
    generation_time_ms: int                  # Time spent generating (for perf tracking)
```

#### TileType Enum

```python
class TileType(int, Enum):
    """Grid tile type representation."""
    EMPTY = 0        # Traversable corridor
    WALL = 1         # Solid wall (impassable)
    PELLET = 2       # Pellet position (collectible)
    POWERUP = 3      # Powerup spawn location
    PACMAN = 4       # Pac-Man spawn (runtime only, not persisted)
    GHOST = 5        # Ghost spawn (runtime only, not persisted)
```

---

### 2. MapConfig

Encapsulates all configuration parameters for map generation.

```python
@dataclass
class MapConfig:
    """Configuration for map generation."""
    
    # Size & Dimensions
    size: Literal["small", "medium", "large"] = "medium"  # Grid preset
    
    # Generation Parameters
    wall_density: float = 0.35          # 0.0-1.0: sparse (open) to dense (maze-like)
    pellet_density: float = 0.80        # 0.0-1.0: sparse to dense pellet placement
    
    # Theme
    theme: Literal["standard", "green_star", "custom"] = "standard"  # Visual style
    
    # Victory Condition
    victory_pellet_percentage: int = 100    # 80-100: % of pellets to collect to win
    
    # Difficulty & Ghost Configuration
    difficulty: Literal["easy", "normal", "hard"] = "normal"
    ghost_count: int = 3                # 2-4: number of ghost spawns on map
    
    # Reproducibility
    seed: Optional[int] = None          # If provided, use for deterministic generation
```

---

### 3. ValidationScore

Records detailed validation metrics and results.

```python
@dataclass
class ValidationScore:
    """Playability validation results."""
    
    # Connectivity Validation
    pellet_reachability: float          # 1.0 = all pellets reachable, 0.0 = none
    all_pellets_reachable: bool         # Hard constraint: True or generation fails
    connectivity_status: str            # "PASS" | "FAIL: isolated pellets at (x,y), ..."
    
    # Ghost Pathfinding Viability
    ghost_navigation_score: float       # 0.0-1.0: % of ghost spawns can reach 50%+ of map
    ghost_path_status: str              # "PASS" | "FAIL: ghost at (x,y) can't navigate"
    
    # Dead-End Trap Detection
    dead_ends_detected: int             # Count of unreachable alcoves
    trap_free: bool                     # True if no unreachable pellet traps
    
    # Layout Quality
    corridor_count: int                 # Number of connected corridor segments
    open_area_percentage: float         # % of non-wall tiles
    
    # Overall Status
    overall_valid: bool                 # True = map is playable
    validation_time_ms: int             # Time spent validating
    check_timestamp: str                # ISO timestamp
```

---

### 4. Theme Asset Registry

Maps tile types and wall patterns to theme-specific visual assets.

```python
@dataclass
class ThemeAssetRegistry:
    """Sprite and asset mappings for a visual theme."""
    
    theme_name: str                             # e.g., "standard", "green_star"
    
    # Tile Sprites
    tile_sprites: Dict[str, str] = {
        "empty": "sprites/themes/{theme}/tile_empty.png",
        "wall": "sprites/themes/{theme}/tile_wall.png",
        "pellet": "sprites/themes/{theme}/tile_pellet.png",
        "powerup_spawn": "sprites/themes/{theme}/tile_powerup_spawn.png",
    }
    
    # Wall Variants (for visual variety within theme)
    wall_variants: Dict[str, List[str]] = {
        "straight_h": ["wall_h_1.png", "wall_h_2.png"],  # Horizontal walls
        "straight_v": ["wall_v_1.png", "wall_v_2.png"],  # Vertical walls
        "corner_nw": ["corner_nw.png"],                   # Corners
        "corner_ne": ["corner_ne.png"],
        "corner_sw": ["corner_sw.png"],
        "corner_se": ["corner_se.png"],
    }
    
    # Entity Sprites
    entity_sprites: Dict[str, str] = {
        "pacman": "sprites/pacman/pacman.png",
        "ghost_red": f"sprites/themes/{theme_name}/ghost_red.png",
        "ghost_blue": f"sprites/themes/{theme_name}/ghost_blue.png",
        "powerup": f"sprites/themes/{theme_name}/powerup.png",
    }
    
    # Color Palette (for runtime recoloring if needed)
    color_palette: Dict[str, str] = {
        "wall": "#1f1f8f",           # Standard blue wall
        "pellet": "#ffb8ae",         # Pink/white pellet
        "background": "#000000",     # Black background
    }
```

---

## Data Flow Diagram

```
MapConfig (user selection)
    ↓
MapGenerator.generate(config)
    ├→ InitializeGrid(size)
    ├→ MazeGeneration(wall_density)
    ├→ PelletPlacement(pellet_density)
    ├→ SpawnPlacement(ghost_count, pacman)
    └→ → GeneratedMap
        ↓
    MapValidator.validate(map)
        ├→ ConnectivityCheck(pellets)
        ├→ GhostPathfindingCheck(spawns)
        ├→ TrapDetection()
        └→ → ValidationScore
        
    If validation passes:
        ↓
    ThemeManager.apply_theme(map, config.theme)
        ├→ LoadThemeAssetRegistry(theme_name)
        ├→ MapTileRenderer(map, registry)
        └→ → Displayable Map Ready for Game
```

---

## Relationships to Existing Entities

### Level (Existing Game Entity)

`GeneratedMap` is composed into the existing `Level` class:

```python
class Level:
    """Existing level entity (modified to support generated maps)."""
    
    source: Literal["json", "generated"]    # NEW: Track origin
    generated_map: Optional[GeneratedMap]   # NEW: Holds procedural map if source="generated"
    
    # ... existing Level fields (width, height, walls, pellets, etc.)
```

---

## Persistence & Storage

### Runtime Storage

- **GeneratedMap instances**: Stored in memory only during game session
- **No persistence**: Maps regenerated fresh each new game (per spec assumption)

### Optional Caching (Future Extension)

If caching future implementations, store JSON representation:

```json
{
  "version": 1,
  "type": "generated_map",
  "width": 16,
  "height": 16,
  "size_preset": "medium",
  "grid": [[0,0,1,1,...], [...], ...],
  "pacman_spawn": [7, 7],
  "ghost_spawns": [[7, 8], [8, 8], [7, 9]],
  "pellet_positions": [[1, 1], [2, 2], ...],
  "config": {
    "size": "medium",
    "wall_density": 0.35,
    "pellet_density": 0.80,
    "theme": "standard",
    "victory_pellet_percentage": 100,
    "difficulty": "normal",
    "ghost_count": 3
  },
  "validation_score": { ... },
  "theme": "standard",
  "seed": null,
  "generation_time_ms": 245
}
```

---

## Validation Constraints

### Hard Constraints (Map fails generation if violated)

1. **Pellet Reachability**: All pellets MUST be reachable from Pac-Man spawn via flood-fill
2. **Ghost Spawn Viability**: All ghost spawns MUST be able to navigate at least 50% of non-wall tiles
3. **No Isolated Regions**: No unreachable alcoves that trap pellets

### Soft Constraints (Used for difficulty scaling)

1. Corridor count >= 3 (more corridors = higher variety)
2. Open area percentage >= 10% (prevents 100% maze density)
3. Ghost spawn separation >= 2 tiles (prevent clustering)

---

## Example Generated Map (JSON)

```json
{
  "type": "GeneratedMap",
  "width": 12,
  "height": 12,
  "size_preset": "small",
  "grid": [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,1],
    [1,1,0,1,1,0,1,0,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,0,1,0,1,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1]
  ],
  "pacman_spawn": [5, 5],
  "ghost_spawns": [[5, 6], [4, 5], [6, 5]],
  "powerup_spawn_points": [[2, 3], [9, 9]],
  "pellet_positions": [[1, 1], [2, 1], [3, 1], [1, 3], ... ],
  "pellet_count": 87,
  "config": {
    "size": "small",
    "wall_density": 0.35,
    "pellet_density": 0.80,
    "theme": "standard",
    "victory_pellet_percentage": 100,
    "difficulty": "normal",
    "ghost_count": 3,
    "seed": null
  },
  "validated": true,
  "validation_score": {
    "pellet_reachability": 1.0,
    "all_pellets_reachable": true,
    "ghost_navigation_score": 0.98,
    "dead_ends_detected": 0,
    "trap_free": true,
    "overall_valid": true,
    "validation_time_ms": 23
  },
  "theme": "standard",
  "generation_time_ms": 245
}
```

---

## Design Notes

1. **Extensibility**: Theme asset registry designed to support custom themes without code changes
2. **Reproducibility**: `seed` field enables deterministic generation for debugging/testing
3. **Validation Transparency**: Scores exposed for diagnostics and difficulty balancing
4. **Backward Compatibility**: Existing `Level` class enhanced, not modified; generated maps wrapped as optional field
