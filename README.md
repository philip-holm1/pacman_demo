# Pacman Demo — Modern Powerups

Run placeholder loop:

```powershell
python -m pacman
```
(After installation via editable mode or src path inclusion; fallback: `python -m src.pacman`.)

Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

Development quickstart: see `specs/001-modern-powerups-pacman/quickstart.md`.

## Movement & Speeds

Fixed timestep: `TICKS_PER_SECOND = 60`.

Player moves every `BASE_PLAYER_MOVE_INTERVAL_TICKS` ticks (default 8) giving ~7.5 tiles/sec. Ghosts move every `GHOST_MOVE_INTERVAL_TICKS` ticks (default 10) giving ~6 tiles/sec (slower than player to allow escaping).

SpeedBoost lowers effective interval:
```
effective_interval = max(1, int(BASE_PLAYER_MOVE_INTERVAL_TICKS / speed_multiplier))
```
Continuous movement persists last direction until blocked or changed.

## Powerup Rules & Controls

Controls:
- Arrow Keys: Move
- P: Pause / Resume
- R: Restart (Victory/Game Over)
- ESC / Window Close: Quit

Powerups:
- SpeedBoost: Increases speed (x1.5).
- GhostFreeze: Stops ghost movement.
- ScoreMultiplier: Stacks x2, x4, x8 (cap at x8).
- InvincibilityBlink: Immune to ghosts; visual blink ~every 0.2s.

Spawn: Attempt every `POWERUP_PELLET_THRESHOLD` pellets; up to 10 placement retries on non-wall, unoccupied tiles.

Duration: Default `DEFAULT_POWERUP_DURATION` seconds. ScoreMultiplier adds a new instance (exponential stacking) rather than refreshing existing.

Pause: Powerup timers freeze because tick count does not advance.

Game States:
- playing: normal updates
- victory / game_over: movement & scoring halt; restart with R

Performance Overlay: Shows FPS and worst frame time (ms) in playing mode.

## Ghost FSM & Intelligent AI (T090)

Ghosts cycle between three modes with intelligent pathfinding:

**Scatter Mode** (default start):
- Each ghost moves toward its assigned corner using Manhattan distance pathfinding
- Corners are assigned per ghost: top-right, top-left, bottom-right, bottom-left
- Direction reconsideration occurs at intersections (3+ valid paths)
- Duration: `SCATTER_DURATION_TICKS = 420` (~7s)

**Chase Mode** (after scatter):
- Ghosts actively pursue the player's current position
- Uses greedy best-first pathfinding (minimize Manhattan distance to player)
- Duration: `CHASE_DURATION_TICKS = 1200` (~20s)
- Alternates back to scatter after duration expires

**Frightened Mode** (triggered by InvincibilityBlink):
- Overrides current cycle state; underlying mode and elapsed cycle ticks are snapshotted
- Random movement using seeded RNG (`frightened_rng`) for determinism
- Duration: `FRIGHTENED_EXTENSION_TICKS = 180` (~3s)
- Extension: Collecting InvincibilityBlink while frightened adds 180 ticks to remaining duration
- On expiry: cycle mode and tick counter restore exactly; cycle resumes from stored position

**Pathfinding & Movement Rules:**
- Ghosts move every `GHOST_MOVE_INTERVAL_TICKS` ticks (default 10 = ~6 tiles/sec)
- Player moves every 8 ticks (~7.5 tiles/sec) - **player is faster** to allow escaping
- Direction chosen to minimize Manhattan distance to target (corner or player)
- No-reversal rule: Ghosts don't reverse direction unless at a dead end or mode change
- Intersection detection: Reconsider direction only when 3+ valid paths available
- Deterministic tie-breaking: Prefer right, left, down, up (in that order)

**Debug HUD Overlay:**
- Enable by setting `GameState.debug_show_ghost_modes = True` to display ghost modes

**GhostFreeze Powerup:**
- Sets ghost state to "frozen", preventing all movement
- Ghost positions remain static while frozen state active
