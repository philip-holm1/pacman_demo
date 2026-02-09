# data-model.md — Modern Powerups (Phase 1)

## Entities

- Player
  - id: string (singleton)
  - position: {x: int, y: int} (tile or pixel coordinates depending on movement system)
  - velocity: {dx: float, dy: float}
  - direction: enum (Up, Down, Left, Right)
  - lives: int
  - score: int
  - active_powerups: list[PowerupInstance]

- Powerup (definition)
  - id: string (type + uid)
  - type: enum {SpeedBoost, GhostFreeze, ScoreMultiplier, InvincibilityBlink}
  - duration_seconds: float
  - value: optional (score bonus or multiplier value)
  - visual_asset_ref: path/string

- PowerupInstance (runtime)
  - powerup_id: string (link to Powerup definition)
  - expires_at_tick: int (game tick index for deterministic expiry)
  - start_tick: int
  - remaining_seconds(game_tick): computed by (expires_at_tick - current_tick) / ticks_per_second

- Ghost
  - id: string
  - position: {x, y}
  - state: enum {normal, frightened, frozen}
  - ai_mode: enum {scatter, chase, random}
  - (FSM runtime fields in GameState, not per Ghost): cycle_mode (scatter|chase), cycle_ticks, frightened_ticks_remaining

- Level
  - id: string
  - tile_grid: 2D array (tile type: wall, floor)
  - pellet_positions: list[{x,y}]
  - powerup_spawn_points: list[{x,y}] (optional)
  - ghost_spawn_points: list[{x,y}]
  - meta: {width, height}

- GameState
  - current_level: Level
  - players: list[Player] (single-player expected)
  - ghosts: list[Ghost]
  - active_powerups: list[PowerupInstance]
  - tick_count: int
  - paused: bool
  - ghost_cycle_mode: string (scatter|chase|frightened)
  - ghost_cycle_ticks: int
  - frightened_ticks_remaining: int
  - _underlying_cycle_mode: string (internal snapshot while frightened)
  - _underlying_cycle_ticks_snapshot: int (internal snapshot while frightened)

## Validation rules
- Player position must be within level bounds and not inside a wall tile.
- Powerup spawns must be on non-blocked tiles and not overlapping actors (retry up to 10 times).
- Powerup durations must be positive and within a configured max (e.g., 120s).
- Score increments must be integers and non-negative.

## State transitions (powerup lifecycle)
1. Spawned on map (Powerup placed) —> Collected by player
2. Collected —> Create PowerupInstance with start_tick and expires_at_tick
3. While active: effect applied each tick by relevant systems (movement, scoring handler)
4. On expiry: remove PowerupInstance and revert affected state (e.g., speed multiplier removed)

## Notes on Timing
- All expiry and durations are tracked by ticks (integer tick counter) rather than wall-clock time. Convert to seconds for UI display using configured ticks-per-second value. This supports determinism and easy pause/resume semantics.

