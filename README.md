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

Player moves every `BASE_PLAYER_MOVE_INTERVAL_TICKS` ticks (default 8) giving ~7.5 tiles/sec. Ghosts move every `GHOST_MOVE_INTERVAL_TICKS` ticks (default 10) giving ~6 tiles/sec.

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
