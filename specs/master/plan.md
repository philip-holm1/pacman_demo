```markdown
# Implementation Plan: Modern Powerups — Pacman (Python)

**Branch**: `master` | **Date**: 2025-11-19 | **Spec**: `/specs/001-modern-powerups-pacman/spec.md`
**Input**: Feature specification located at `/specs/001-modern-powerups-pacman/spec.md`

## Summary

Implement a local, deterministic single-player Pacman demo in Python that adds a modern powerup system while preserving the retro feel. Deliverables: runtime implementation of four powerups (`SpeedBoost`, `GhostFreeze`, `ScoreMultiplier`, `InvincibilityBlink`), HUD for active effects/timers, deterministic spawn logic (pellet-threshold driven), local high-score persistence, and a minimal automated test set for core mechanics.

Technical approach: use a lightweight Python game library for rendering and input, small file-based storage for persistence, fixed-timestep game loop (target 60 FPS) for determinism, and pytest for unit tests. Keep the project single-repo, single-package for simplicity and fast iteration.

## Technical Context

**Language/Version**: Python 3.11 (target; accept 3.10 where needed)
**Primary Dependencies**: `pygame` (rendering/input/audio), `pytest` (tests), `pyyaml` or built-in `json` (level/config parsing). Optional dev tools: `black`, `ruff`.
**Storage**: Local JSON files for level data (`levels/level1.json`) and highscore (`data/highscore.json`). Assets under `assets/` directory.
**Testing**: `pytest` for unit tests; focus on deterministic logic (collision, powerup timers, spawn rules). Simple integration script for smoke-test playthroughs.
**Target Platform**: Desktop platforms (Windows primary for development, also Linux/macOS supported). No network or cloud required (constitution: local-first).
**Project Type**: Single local game project (library + small runner). Source layout under `src/` with a small CLI/runner at repo root.
**Performance Goals**: Target stable 60 FPS on typical development machines; accept 30 FPS minimum. Use a fixed-timestep update loop to ensure deterministic behavior across runs.
**Constraints**: Offline-first, deterministic tick behavior, minimal asset set, no external services. Game must pause/resume and freeze timers during pause. Powerups cannot rely on non-deterministic timers.
**Scale/Scope**: Small demo (single level shipped, single-player local). Codebase expected to be <5k LOC initially.

## Constitution Check

Gates (from `.specify/memory/constitution.md`) and evaluation:

- Gate: Local-first & no network — PASS (no network planned).
- Gate: Deterministic behavior — PASS (fixed-timestep loop required in design).
- Gate: Testable core units — PASS (pytest planned for collision, scoring, powerup timers, spawn logic).
- Gate: One playable level & assets — PASS (deliver `levels/level1.json` and minimal `assets/`).
- Gate: Pause/Resume behavior — PASS (design will pause timers and effects).

All constitution gates are satisfied by this plan. No violations identified.

## Project Structure

Documentation and design files for this feature (created by this plan):

```
specs/001-modern-powerups-pacman/
├── spec.md
├── spec_filled.md
└── checklists/

specs/master/
├── plan.md            # this file (implementation plan)
├── research.md        # Phase 0 output
├── data-model.md      # Phase 1 output
├── quickstart.md      # Phase 1 output
└── contracts/         # Phase 1 output (module contracts)
```

Suggested source layout (single project):

```
src/
├── pacman/                # package root
│   ├── __main__.py        # runner (python -m pacman)
│   ├── game.py            # main game loop & orchestration
│   ├── entities/          # Player, Ghost, Powerup, Pellet models
│   ├── systems/           # collision, spawn, powerup managers
│   ├── levels/            # level loader
│   └── assets/            # sprite ref helpers
tests/
├── unit/
│   ├── test_collision.py
│   ├── test_powerup_timers.py
│   └── test_spawn_logic.py
assets/
├── sprites/
└── sounds/
levels/
└── level1.json
data/
└── highscore.json
```

**Structure Decision**: Single Python package reduces complexity, supports fast iteration, and aligns with constitution (local, testable, deterministic). `pygame` will be used for input/render/audio and kept behind a thin rendering/IO layer to allow easier unit testing of logic.

## Phase Breakdown (high level)

Phase 0 — Research: choose libraries, finalize deterministic loop strategy, powerup timer implementation choices, and spawn strategy. Output: `research.md` (this plan includes resolved clarifications).

Phase 1 — Design: produce `data-model.md`, module contracts under `contracts/`, and `quickstart.md`. Update agent context. Implement minimal `levels/level1.json` and placeholder assets.

Phase 2 — Implementation & Tests: implement game loop, entities, powerup manager, HUD, persistence, and tests. Ship playable demo and acceptance tests.

## Complexity Tracking

No constitution violations; no additional complexity justifications required at this time.

```
directories captured above]
