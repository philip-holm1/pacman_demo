# tasks.md — Modern Powerups — Pacman (Python)

Feature: Modern Powerups — Pacman (Single-player)
Spec: `/specs/001-modern-powerups-pacman/spec.md`
Plan: `/specs/001-modern-powerups-pacman/plan.md`

## Phase 1: Setup (Project Initialization)
Goal: Establish repository structure, dependencies, baseline config, and placeholder assets to enable iterative development.
Independent Test Criteria: Able to run `python -m pacman` (placeholder loop), load `levels/level1.json`, display a window, quit cleanly.

### Tasks
 - [X] T001 Create `requirements.txt` with pygame, pytest, ruff, black in repo root
 - [X] T002 Initialize `src/pacman/__init__.py` and `src/pacman/__main__.py` with placeholder main loop (prints tick count then exits)
 - [X] T003 Create `src/pacman/game.py` with fixed-timestep loop skeleton (no entities yet)
 - [X] T004 Create directories `src/pacman/entities`, `src/pacman/systems`, `src/pacman/levels`, `assets/sprites`, `assets/sounds`, `data`, `levels`
 - [X] T005 [P] Add placeholder level file `levels/level1.json` with grid, pellet positions, ghost/player spawn placeholders
 - [X] T006 [P] Add placeholder high score file `data/highscore.json` with `{ "highscore": 0 }`
 - [X] T007 [P] Add placeholder sprite assets README `assets/sprites/README.md` describing required art stubs
 - [X] T008 Add `README.md` top-level with run/test instructions referencing quickstart
 - [X] T009 Add `src/pacman/config.py` with constants (TICKS_PER_SECOND, DEFAULT_POWERUP_DURATION, START_LIVES)
 - [X] T010 Configure basic `pyproject.toml` (tool.black, tool.ruff) for formatting (optional dev tooling)

## Phase 2: Foundational (Blocking Prerequisites)
Goal: Core structures (entities, level loader, collision utility, event bus) required before powerups or scoring logic.
Independent Test Criteria: Unit tests pass for level loading and collision; player moves inside bounds; pause/resume toggles loop state.

### Tasks
- [ ] T011 Implement `src/pacman/levels/loader.py` to parse `levels/level1.json` into Level object
- [ ] T012 Implement `src/pacman/entities/player.py` with position, velocity, direction, lives, score fields
- [ ] T013 Implement `src/pacman/entities/ghost.py` with position, state enum
- [ ] T014 [P] Implement `src/pacman/entities/powerup.py` (definition + instance class)
- [ ] T015 Implement `src/pacman/systems/event_bus.py` lightweight synchronous event dispatcher
- [ ] T016 Implement `src/pacman/systems/collision.py` for tile-based collision and pellet collection detection
- [ ] T062 Implement life decrement on ghost collision (extend `collision.py` to detect ghost contact; inactive during InvincibilityBlink)
- [ ] T063 Add unit test `tests/unit/test_life_decrement.py` verifying lives reduce, not below zero, and ignored during InvincibilityBlink
- [ ] T017 Implement `src/pacman/systems/game_state.py` aggregate state container (tick_count, paused, references to entities)
- [ ] T018 Integrate player movement handling in `game.py` with keyboard input abstraction
- [ ] T019 Add pause/resume handling in `game.py` (P key) freezing tick advancement
- [ ] T020 Add unit test `tests/unit/test_level_loader.py` for loader correctness (pellet count, dimensions)
- [ ] T021 [P] Add unit test `tests/unit/test_collision.py` for wall vs pellet detection
- [ ] T022 Add unit test `tests/unit/test_pause.py` ensuring paused state stops tick increment
 - [X] T011 Implement `src/pacman/levels/loader.py` to parse `levels/level1.json` into Level object
 - [X] T012 Implement `src/pacman/entities/player.py` with position, velocity, direction, lives, score fields
 - [X] T013 Implement `src/pacman/entities/ghost.py` with position, state enum
 - [X] T014 [P] Implement `src/pacman/entities/powerup.py` (definition + instance class)
 - [X] T015 Implement `src/pacman/systems/event_bus.py` lightweight synchronous event dispatcher
 - [X] T016 Implement `src/pacman/systems/collision.py` for tile-based collision and pellet collection detection
 - [X] T062 Implement life decrement on ghost collision (extend `collision.py` to detect ghost contact; inactive during InvincibilityBlink)
 - [X] T063 Add unit test `tests/unit/test_life_decrement.py` verifying lives reduce, not below zero, and ignored during InvincibilityBlink
 - [X] T017 Implement `src/pacman/systems/game_state.py` aggregate state container (tick_count, paused, references to entities)
 - [X] T018 Integrate player movement handling in `game.py` with keyboard input abstraction
 - [X] T019 Add pause/resume handling in `game.py` (P key) freezing tick advancement
 - [X] T020 Add unit test `tests/unit/test_level_loader.py` for loader correctness (pellet count, dimensions)
 - [X] T021 [P] Add unit test `tests/unit/test_collision.py` for wall vs pellet detection
 - [X] T022 Add unit test `tests/unit/test_pause.py` ensuring paused state stops tick increment

## Phase 3: User Story US1 — Start & Play (Priority P1)
Story Goal: Player can start a local game, control Pacman, collect pellets, and complete the level.
Independent Test Criteria: Start game → move player → collect all pellets → victory screen triggers.

### Tasks
 - [X] T023 [US1] Implement pellet data structure and integrate pellet removal into collision system (`src/pacman/systems/collision.py`)
 - [X] T064 [US1] Implement game over screen state (`src/pacman/systems/screens.py`) with restart prompt (R key) (loss path available in MVP)
 - [X] T065 [US1] Add unit test `tests/unit/test_game_over_restart_flow.py` verifying game over triggers at 0 lives and restart resets state (high score persists)
 - [X] T024 [P] [US1] Add HUD basic overlay for score and lives (`src/pacman/systems/hud.py`)
 - [X] T025 [US1] Implement level completion check in `game.py` (when pellet list empty)
 - [X] T026 [US1] Implement victory screen state (`src/pacman/systems/screens.py`) with restart prompt
 - [X] T027 [US1] Implement restart handling (R key) resetting GameState
 - [X] T028 [P] [US1] Add unit test `tests/unit/test_level_completion.py` for pellet exhaustion triggers
 - [X] T029 [US1] Add integration test `tests/unit/test_restart_after_victory_and_game_over.py` verifying restart resets score, pellets, and lives from both victory and game over

## Phase 4: User Story US2 — Powerup Interaction (Priority P1)
Story Goal: Player collects powerups that modify gameplay with concurrent effects and visible timers.
Independent Test Criteria: Collect each powerup type; observe effect start, timer progression, concurrent behaviors; expiry reverts state.

### Tasks
 - [X] T030 [US2] Implement `src/pacman/systems/powerup_manager.py` with spawn, collect, update APIs (per contract)
 - [X] T031 [P] [US2] Implement pellet-threshold spawn logic (every N pellets) inside powerup_manager
 - [X] T032 [US2] Integrate powerup spawn call into main loop after threshold check (`game.py`)
 - [X] T033 [US2] Implement SpeedBoost effect application (player velocity multiplier) inside update_powerups (placeholder multiplier stored)
 - [X] T034 [US2] Implement GhostFreeze effect (ghost state frozen) inside update_powerups
 - [X] T035 [US2] Implement ScoreMultiplier stacking and duration refresh rules
 - [X] T036 [US2] Implement InvincibilityBlink effect (ignore ghost collision) with visual indicator
 - [X] T037 [P] [US2] Implement powerup HUD timers and progress bars (`src/pacman/systems/hud_powerups.py`)
 - [X] T038 [US2] Integrate event bus events for collected/expired (`event_bus.py` → used in HUD updates)
 - [X] T039 [US2] Add unit test `tests/unit/test_powerup_spawn_threshold_and_retry.py` (threshold trigger, valid tile, retry cap)
 - [X] T040 [US2] Add unit test `tests/unit/test_powerup_duration_refresh.py` (same-type refresh behavior)
 - [X] T041 [US2] Add unit test `tests/unit/test_score_multiplier_stack.py` (x2 → x4 stacking scenario)
 - [X] T042 [P] [US2] Add unit test `tests/unit/test_powerup_expiry.py` (expires_at_tick removal)
 - [X] T043 [US2] Add unit test `tests/unit/test_concurrent_powerups.py` (speed + freeze independent)
 - [X] T066 [US2] Add unit test `tests/unit/test_powerup_spawn_overlap_avoidance.py` (skip after 10 failed placements on occupied tiles)
 - [X] T067 [US2] Add unit test `tests/unit/test_powerup_timer_accuracy.py` (±0.5s display vs tick-based remaining)
 - [X] T068 [US2] Add unit test `tests/unit/test_pause_timer_ui_freeze.py` (no visual decrement while paused)
 - [X] T069 [US2] Add unit test `tests/unit/test_invincibility_blink_interval.py` (blink toggles ~every 0.2s)
 - [X] T070 [US2] Add unit test `tests/unit/test_ghost_freeze_no_movement.py` (ghost positions unchanged while frozen)
 - [X] T071 [US2] Add unit test `tests/unit/test_ghost_freeze_no_score_change.py` (score unaffected by freeze alone)
 - [X] T072 [US2] Add unit test `tests/unit/test_score_multiplier_cap.py` (cap at x8)

## Phase 5: User Story US3 — Score & Feedback (Priority P2)
Story Goal: Immediate visual/audio feedback for scoring & powerup pickups; scoreboard updates correctly including multipliers.
Independent Test Criteria: Collect pellet & powerup; see score change, animation, and sound; multiplier affects scoring.

### Tasks
- [X] T044 [US3] Implement scoring system module `src/pacman/systems/scoring.py` (base pellet value, powerup bonuses, multiplier application)
- [X] T045 [P] [US3] Add floating text feedback for score changes (`hud.py` or separate `hud_feedback.py`)
- [X] T046 [US3] Integrate audio playback for powerup pickup (0.5s sound) `src/pacman/systems/audio.py` (stub implementation)
- [X] T047 [US3] Integrate retro animation trigger for each powerup pickup (`hud_powerups.py`) (placeholder data in feedback list)
- [X] T048 [US3] Add high score load/save functions `src/pacman/systems/highscore.py`
- [X] T049 [US3] Integrate high score display in main menu / victory screen
- [X] T050 [US3] Add unit test `tests/unit/test_scoring_multiplier.py` verifying multiplier math
- [X] T051 [US3] Add unit test `tests/unit/test_highscore_persistence.py` verifying write & read fallback
- [X] T052 [US3] Add unit test `tests/unit/test_feedback_visual.py` (animation list appended on score change)

## Phase 6: Polish & Cross-Cutting
Goal: Performance tuning, code quality, documentation, and extended stability tests.
Independent Test Criteria: All unit tests pass; manual playtest shows stable 30–60 FPS; no crashes in 30 min continuous run.

### Tasks
- [ ] T053 Add performance measurement tick counter & simple FPS overlay `src/pacman/systems/perf.py`
 - [X] T053 Add performance measurement tick counter & simple FPS overlay `src/pacman/systems/perf.py`
- [ ] T054 [P] Add ruff & black enforcement pre-commit config `.pre-commit-config.yaml`
- [ ] T055 Refactor any duplicated logic in powerup_manager (spawn & expiry) into helper functions
- [ ] T056 Add automated smoke script `scripts/run_smoke_playtest.py` moving player randomly for 5 minutes
- [ ] T057 Add test `tests/unit/test_pause_powerup_timer.py` verifying timers freeze during pause
- [ ] T058 Add test `tests/unit/test_invincibility_collision.py` ghost collision ignored during InvincibilityBlink
- [ ] T059 Update README with powerup rules & controls section
- [ ] T060 [P] Add docstring coverage check script `scripts/check_docstrings.py`
- [ ] T061 Final manual QA checklist markdown `specs/001-modern-powerups-pacman/checklists/qa_playtest.md`
- [ ] T073 Add long-run stability script `scripts/run_stability_test.py` (60-minute randomized movement)
- [ ] T074 Add performance assertion harness `scripts/verify_performance.py` (parse frame log, enforce thresholds)
- [ ] T075 Add ghost movement AI system `src/pacman/systems/ghost_ai.py` updating ghosts each tick (deterministic order, respects walls, frozen state)
- [ ] T076 Add unit test `tests/unit/test_ghost_movement_wall_avoidance.py` verifying ghosts never enter wall tiles and remain static when frozen
 - [X] T077 Improve game over logic: block player movement & scoring when mode=game_over; single high score update
 - [X] T078 Add enhanced game over screen overlay with round score and restart prompt + test `tests/unit/test_game_over_freeze.py`

## Dependencies & Order
Story Completion Order: US1 (core loop) → US2 (powerup mechanics) → US3 (feedback & scoring polish) → Polish.
Foundational must complete before US1 tasks commence (T011–T022). Setup must complete before Foundational.

## Parallel Execution Examples
- Setup: T005, T006, T007 can run in parallel after directory creation (T004).
- Foundational: T014 (powerup entity) and T021 (collision test) parallel with T018 player movement.
- US2: T031 (spawn logic) parallel with T033–T034 effect implementations; T037 HUD timers parallel with T035 multiplier logic.
- US3: T045 floating text and T046 audio integration can proceed in parallel once scoring system skeleton (T044) exists.
- Polish: T054 tooling parallel with T056 smoke script and T058 invincibility test.

## Implementation Strategy (MVP First)
MVP Scope: Complete through US1 (T001–T029). This yields a playable level with movement, pellet collection, victory, and restart. Deliver US2 & US3 incrementally after MVP validation.

Post-MVP Increment Steps:
1. Add powerup concurrency & timer HUD (US2)
2. Add scoring multiplier + feedback animations (US3)
3. Polish performance & persistence (Polish phase)

## Task Count Summary
- Setup: 10 tasks
- Foundational: 14 tasks (T011–T022, T062–T063)
- US1: 9 tasks (T023–T029, T064–T065)
- US2: 21 tasks (T030–T043, T066–T072)
- US3: 9 tasks (T044–T052)
- Polish: 11 tasks (T053–T061, T073–T074)
Total: 74 tasks

## Format Validation
All tasks follow required format: `- [ ] T### [P]? [US#]? Description with file path`. Non-story phases omit story labels. Parallelizable tasks marked `[P]` only when independent (different files, no unmet dependencies).

## Independent Test Criteria Recap
- US1: Start, control, collect pellets, victory triggers, lives decrement on ghost collisions, game over at 0 lives, restart after game over.
- US2: Collect each powerup; timer & effect concurrency validated; expiry reverts state; spawn threshold & retry; overlap avoidance skip; timer accuracy ±0.5s; blink every ~0.2s; multiplier cap; ghost freeze effects.
- US3: Score updates with multiplier; audio + animation feedback visible; high score persists (fallback logged on write failure).
- Polish: Long-run (60 min) stability; performance thresholds (avg FPS ≥30, 95th percentile frame time ≤2× target); pause timer UI freeze.

## MVP Confirmation
MVP = US1 core loop plus constitution-critical lives & game over (T062–T065). Parallelizable tasks flagged to accelerate delivery.

---
End of tasks.md
