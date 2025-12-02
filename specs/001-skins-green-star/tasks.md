# Tasks — Green Star Skins

Feature: Green Star Skins

## Phase 1 — Setup

- [ ] T001 Create project structure for skin assets at `assets/sprites/skins/green_star/`
- [ ] T002 Add skin preference key in `src/pacman/config.py`
- [ ] T003 Wire reading of skin preference in `src/pacman/game.py`
- [ ] T004 Document selection flow in `specs/001-skins-green-star/quickstart.md`

## Phase 2 — Foundational

- [ ] T005 Add skin contract config parsing in `src/pacman/config.py`
- [ ] T006 Implement asset loader override mapping in `src/pacman/game.py`
- [ ] T007 Ensure default fallback on missing assets in `src/pacman/game.py`

## Phase 3 — [US1] Select and play with Green Star skin (P1)

Goal: Enable the Green Star skin and apply themed visuals to player, ghosts, powerups, and pellets without changing gameplay.

Independent Test Criteria: Selecting the skin shows themed visuals for all categories in level 1 without affecting mechanics or timing.

- [ ] T008 [P] [US1] Add player sprite override (green star) in `src/pacman/entities/player.py`
- [ ] T009 [P] [US1] Add ghost visuals (comet tails) in `src/pacman/entities/ghost.py`
- [ ] T010 [P] [US1] Add powerup visuals (star shards) in `src/pacman/entities/powerup.py`
- [ ] T011 [P] [US1] Add pellet visuals (stardust dots) in `src/pacman/game.py` (or the renderer responsible for pellets)
- [ ] T012 [US1] Integrate skin selection into main menu settings in `src/pacman/game.py`

## Phase 4 — [US2] Skin persists and can be changed (P2)

Goal: Allow switching between default and Green Star skins via main menu Settings and persist choice across restarts.

Independent Test Criteria: Change skin, restart game, selected skin remains active; revert to default and confirm persistence.

- [ ] T013 [US2] Persist selected skin in `data/settings.json`
- [ ] T014 [P] [US2] Load persisted selection in `src/pacman/config.py`
- [ ] T015 [US2] Update main menu flow in `src/pacman/game.py`

## Phase 5 — [US3] Accessibility and clarity (P3)

Goal: Ensure themed visuals are readable and special states remain distinguishable.

Independent Test Criteria: Frightened ghosts and invincibility feedback are visually clear with the skin enabled.

- [ ] T016 [US3] Implement frightened ghost visual variant in `src/pacman/entities/ghost.py`
- [ ] T017 [US3] Implement invincibility feedback compatibility in `src/pacman/entities/player.py`

## Final Phase — Polish & Cross-Cutting

- [ ] T018 Add asset previews to Settings in `src/pacman/game.py`
- [ ] T019 Verify performance impact and frame timing in `scripts/verify_performance.py`
- [ ] T020 Validate fallback behavior for missing assets in `src/pacman/game.py`
 - [ ] T021 Add unit test `tests/unit/test_skin_settings_preview.py` to verify Settings preview loads correct assets without blocking.
 - [ ] T022 Add unit test `tests/unit/test_visuals_only_behavior.py` to assert collisions and timing unchanged when skin toggled.

## Dependencies

- US1 → US2 → US3
- T001 → T005 → T008–T012
- T002 → T003 → T006–T007
- T013 → T014 → T015
- T016 → T017

## Parallel Execution Examples

- [P] T008, T009, T010 can be implemented concurrently (different files).
- [P] T011 can run in parallel with T008–T010 if pellet rendering is independent.
- [P] T014 can run in parallel with T015 once T013 exists.

## Implementation Strategy

- MVP first: Complete Phase 3 (US1) to demonstrate themed visuals end-to-end.
- Incremental delivery: Add persistence (US2), then accessibility refinements (US3).
