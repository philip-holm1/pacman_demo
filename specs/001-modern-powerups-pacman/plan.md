```markdown
# Implementation Plan: Modern Powerups — Pacman (Python)

**Branch**: `001-modern-powerups-pacman` | **Date**: 2025-11-19 | **Spec**: `/specs/001-modern-powerups-pacman/spec.md`
**Input**: Feature specification located at `/specs/001-modern-powerups-pacman/spec.md`

## Summary

Implement a local, deterministic single-player Pacman demo in Python that adds a modern powerup system while preserving the retro feel. Deliverables: runtime implementation of four powerups (`SpeedBoost`, `GhostFreeze`, `ScoreMultiplier`, `InvincibilityBlink`), HUD for active effects/timers, deterministic spawn logic (pellet-threshold driven, empty walkable tile placement), local high-score persistence, ghost FSM (Scatter/Chase/Frightened) with InvincibilityBlink-triggered Frightened + 3s extension, and a comprehensive automated test set for core mechanics.

Technical approach: use `pygame` for rendering/input/audio, small file-based storage for persistence, a fixed-timestep core loop at 60 ticks per second (FR-016) decoupled from render FPS, and pytest for unit tests. Keep the project single-repo, single-package for simplicity and fast iteration. All temporal mechanics (powerup durations, blink cadence, ghost decision cadence, frightened extension) derive from tick counts for determinism.

## Technical Context

**Language/Version**: Python 3.11 (target; accept 3.10 where needed)
**Primary Dependencies**: `pygame` (rendering/input/audio), `pytest` (tests), `pyyaml` or built-in `json` (level/config parsing). Optional dev tools: `black`, `ruff`.
**Storage**: Local JSON files for level data (`levels/level1.json`) and highscore (`data/highscore.json`). Assets under `assets/` directory.
**Testing**: `pytest` for unit tests; focus on deterministic logic (collision, powerup timers, spawn rules). Simple integration script for smoke-test playthroughs.
**Target Platform**: Desktop platforms (Windows primary for development, also Linux/macOS supported). No network or cloud required (constitution: local-first).
**Project Type**: Single local game project (library + small runner). Source layout under `src/` with a small CLI/runner at repo root.
**Performance Goals**: Core logic at fixed 60 ticks/sec (FR-016). Rendering aims for ~60 FPS; acceptable degradation to 30 FPS with no impact on tick-driven timers. Performance tracker records tick processing times; 95th percentile tick duration ≤ 2× nominal tick budget. Jitter tolerance: ≤1 tick drift averaged over any 5s window.
**Constraints**: Offline-first, deterministic tick behavior, minimal asset set, no external services. Game must pause/resume and freeze timers (HUD timers visually stop). Powerups & ghost FSM cannot rely on wall-clock time—only tick counts. RNG for spawn tile selection seeded once per run (e.g., `random.seed(LEVEL_SEED)`); optional spawn log enables replay.
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
├── plan.md            # this file (implementation plan)
├── research.md        # Phase 0 output
├── data-model.md      # Phase 1 output
├── quickstart.md      # Phase 1 output
├── contracts/         # Phase 1 output (module contracts)
└── checklists/
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

Phase 2 — Implementation & Tests: implement game loop (fixed 60 TPS), entities, powerup manager (empty-tile spawn, FR-017 rules), HUD, ghost FSM (FR-018), frightened trigger/extension on InvincibilityBlink, persistence, and core tests (spawn overlap avoidance & timer accuracy, ghost mode transitions, frightened extension timing, decision cadence determinism). NOTE: Lives decrement logic is elevated into Foundational; Game Over screen & restart integrated early in US1 to satisfy constitution minimal loop (win + loss paths before powerups).

## Complexity Tracking

No constitution violations; no additional complexity justifications required at this time.

### Stability & Measurement Addendum

Long-run stability validated via a 60-minute automated movement script (random direction changes at fixed intervals). Performance harness computes tick processing latency and derived FPS; failure thresholds trigger test failure. Determinism documented via seed value captured in run log. Timer accuracy, blink cadence, ghost decision cadence, frightened extension, and powerup expiry tests verify SC-003, FR-014, FR-016–FR-018.

### Added Functional Requirements Reflected

- FR-016: Fixed 60 ticks/sec loop—update loop module to expose `TICKS_PER_SECOND` constant; tests assert drift bounds.
- FR-017: Powerups spawn on empty walkable tiles—spawn manager selects from filtered floor set; no pellet mutation; tests confirm pellet counts invariant pre/post uncollected expiry.
- FR-018: Ghost FSM—implement mode field, timers for scatter/chase cycle (defaults pending), frightened on InvincibilityBlink + 3s extension (tick-based), decision cadence every 10 ticks with deterministic tie-break.

### New Test Additions

- test_tick_loop_stability.py: asserts 60 TPS over simulated 5s window within jitter tolerance.
- test_powerup_empty_tile_spawn.py: verifies spawn never occupies pellet tile & pellet count unchanged after expiry.
- test_ghost_fsm_modes.py: transitions scatter→chase, forced frightened trigger, extension timing (remaining + 180 ticks), exit back to cycle.
- test_ghost_decision_cadence.py: ensures direction changes only on scheduled decision ticks.
- test_frightened_randomness_seeded.py: with fixed seed, sequence is reproducible; verifies uniform choice distribution over sample window.

### Implementation Tasks (Delta)

1. Introduce `constants.py` or extend existing config with `TICKS_PER_SECOND=60`, `GHOST_DECISION_INTERVAL_TICKS=10`, `FRIGHTENED_EXTENSION_TICKS=180`.
2. Refactor game loop to separate logic tick from render frame; ensure pause halts tick progression.
3. Update powerup spawn manager: filter candidate floor tiles; exclude pellets; maintain deterministic candidate list ordering.
4. Extend ghost entity: add `mode`, `mode_ticks_remaining`; integrate FSM update in tick loop.
5. Implement frightened trigger hook in powerup collection for InvincibilityBlink; schedule extension ticks.
6. Add tests listed above; seed RNG in test setup for deterministic assertions.
7. Update HUD to show ghost modes optionally (debug overlay) for test visibility (toggle flag).
8. Performance tracker: log tick durations separately from frame durations.

```
directories captured above]
