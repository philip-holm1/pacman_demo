# Pacman Demo — Constitution (Minimal, Local Game)

This document lists the bare-minimum, non-negotiable requirements for the local (single-machine) Pacman demo to be playable, testable, and maintainable.

## Core Principles

- Minimal: implement only what's required for a playable local experience.
- Deterministic: game behavior should be deterministic given the same inputs (for easier testing/debugging).
- Local-first: no network, multiplayer servers, or cloud dependencies required to run or test the game.
- Testable: small, focused units (collision, scoring, input handling) must be covered by tests or simple runtime checks.

## Gameplay Requirements (Bare Minimum)

- Players: single-player only.
- Objective: Player navigates a maze and collects all dots.
- Lives: player starts with 3 lives (configurable); losing all lives → game over.
- Win condition: all dots cleared → victory screen.
- Lose condition: no lives remaining → game over screen with option to restart.
- Pause/Resume: must be possible via a single key (e.g., `P` or `Esc`).

## Controls

- Primary input: keyboard.
	- Movement: Arrow keys or `W`/`A`/`S`/`D` (both supported if implemented). Use whichever is simplest for the platform.
	- Pause: `P` or `Esc`.
	- Restart after game over: `R` (or show on-screen prompt to restart).
- Input must be polled each frame and applied in the next game tick (no blocking reads).

## Game Loop and Performance

- Target framerate: 60 FPS if feasible; if not, stable 30 FPS is acceptable.
- Game loop: fixed-timestep update (recommended) or simple frame-based update with delta time.
- Time/physics: movement and collisions must behave consistently across runs on the same machine.

## Assets and Layout

- Assets: use a minimal, clearly organized set under `assets/`:
	- `assets/sprites/` — player, enemies, pellets, walls.
	- `assets/sounds/` — optional; audio may be stubbed if not available.
- Level: include one playable level file (e.g., `levels/level1.json`) describing walls, pellet positions, player/enemy start positions.

## Scoring & Progress

- Score increments for collecting pellets and special items (if present).
- Display: current score and remaining lives must be visible during play.
- High score persistence: optional for bare minimum; if implemented, store locally in a single small file (e.g., `highscore.json`). Document fallback if write fails.

## Persistence & Config

- Configurable values (in a small JSON/text file or constants): starting lives, framerate cap, input mapping (optional).
- No external databases or services.

## Save/Load

- Not required for the bare minimum. If implemented, must be local and optional.

## Testing & Acceptance Criteria

- Manual acceptance test (happy path):
	1. Launch game locally.
	2. Player can move and collect pellets.
	3. When all pellets are collected, victory condition triggers.
	4. When player loses all lives, game over triggers and restart is possible.
	5. Pause/resume works.
- Automated unit tests (recommended minimal set):
	- Collision detection between player and pellet returns expected result.
	- Scoring increments when pellet is collected.
	- Life decrement when player collides with enemy.
	- Level load from `levels/level1.json` produces expected map bounds and pellet count.

## Development Workflow (Minimal)

- Local run: `npm start` / `python -m ...` or the project's existing runner. No network required.
- Keep changes small and focused; add tests for any new game logic.

## Governance

- This constitution defines the minimal acceptable behavior for a local playable demo. Any deviation (e.g., adding networked multiplayer) requires updating this document and adding integration tests.

**Version**: 1.0.0 | **Ratified**: 2025-11-17 | **Last Amended**: 2025-11-17

--
Notes: This file intentionally keeps scope small to enable a quick, local playable demo. If you want, I can expand sections into checklists or add a minimal `levels/level1.json` and demo assets next.
