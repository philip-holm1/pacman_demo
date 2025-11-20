```markdown
# Implementation Plan: Modern Powerups — Pacman (Python)

**Branch**: `001-modern-powerups-pacman` | **Date**: 2025-11-19 | **Spec**: `/specs/001-modern-powerups-pacman/spec.md`
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
**Performance Goals**: Target stable 60 FPS; accept 30 FPS minimum. Fixed-timestep loop ensures determinism. Frame time logger will record per-tick durations; 95th percentile frame time ≤ 2× target frame time.
**Constraints**: Offline-first, deterministic tick behavior, minimal asset set, no external services. Game must pause/resume and freeze timers (HUD timers visually stop). Powerups cannot rely on non-deterministic timers. RNG for spawn tile selection seeded once per run (e.g., `random.seed(LEVEL_SEED)`); optional spawn log enables replay.
**Scale/Scope**: Small demo (single level shipped, single-player local). Codebase expected to be <5k LOC initially.

## Constitution Check

Gates (from `.specify/memory/constitution.md`) and evaluation:

- Gate: Local-first & no network — PASS (no network planned).
- Gate: Deterministic behavior — PASS (fixed-timestep loop required in design).
- Gate: Testable core units — PASS (pytest planned for collision, scoring, powerup timers, spawn logic).
- Gate: One playable level & assets — PASS (deliver `levels/level1.json` and minimal `assets/`).
- Gate: Pause/Resume behavior — PASS (design will pause timers and effects; HUD timers freeze visually).
- Gate: Lives/Game Over — PASS (lives decrement & game over state in spec FR-012/FR-013).

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

**Structure Decision**: Single Python package reduces complexity, supports fast iteration, and aligns with constitution (local, testable, deterministic). `pygame` behind thin rendering layer enables unit tests. Timer accuracy validated against tick count; InvincibilityBlink blink cadence (0.2s) derived from tick interval; multiplier cap logic enforced in scoring tests; spawn retry capped at 10 with skip fallback.

## Phase Breakdown (high level)

Phase 0 — Research: choose libraries, finalize deterministic loop strategy, powerup timer implementation choices, and spawn strategy. Output: `research.md` (this plan includes resolved clarifications).

Phase 1 — Design: produce `data-model.md`, module contracts under `contracts/`, and `quickstart.md`. Update agent context. Implement minimal `levels/level1.json` and placeholder assets.

Phase 2 — Implementation & Tests: implement game loop, entities, powerup manager, HUD, persistence, lives & game over logic, and tests (spawn overlap avoidance & timer accuracy). Ship playable demo and acceptance tests.

## Complexity Tracking

No constitution violations; no additional complexity justifications required at this time.

### Stability & Measurement Addendum

Long-run stability validated via a 60-minute automated movement script (random direction changes at fixed intervals). Performance harness computes average FPS and percentile frame times; failure thresholds trigger test failure. Determinism documented via seed value captured in run log. Timer accuracy and blink cadence tests verify SC-003 and FR-014.

```
directories captured above]
