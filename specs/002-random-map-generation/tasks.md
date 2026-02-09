# Development Tasks: Random Map Generation and Playable Levels

**Feature**: Random Map Generation and Playable Levels  
**Branch**: `002-random-map-generation`  
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)  
**Total Tasks**: 85 | **Phases**: 6  

---

## Phase 1: Setup & Infrastructure

*Project initialization and foundational scaffolding*

- [ ] T001 Create generators module directory structure in `src/pacman/generators/`
- [ ] T002 Create `src/pacman/generators/__init__.py` with module exports
- [ ] T003 [P] Create `src/pacman/generators/config.py` for MapConfig dataclass (size, density, theme)
- [ ] T004 Create unit test directory structure in `tests/unit/` for generator tests
- [ ] T005 Document mapping between spec requirements and implementation tasks in IMPLEMENTATION.md

---

## Phase 2: Foundational (Blocking Prerequisites)

*Core validation and generation infrastructure that enables all user stories*

- [ ] T006 [P] Implement `src/pacman/generators/validator.py` with MapValidator base class
- [ ] T007 [P] Implement connectivity check algorithm (BFS flood-fill) in `validator.py` to ensure all pellets reachable
- [ ] T008 [P] Implement ghost pathfinding viability check in `validator.py` (A* pathfinding test)
- [ ] T009 [P] Create `src/pacman/generators/playability_check.py` for validation orchestration
- [ ] T010 [P] Create fallback level pool: identify and catalog vetted hand-crafted levels in `levels/fallback/`
- [ ] T011 Create `src/pacman/generators/map_schema.py` with GeneratedMap dataclass (grid, spawns, validator result)
- [ ] T012 [P] Unit tests for connectivity validation in `tests/unit/test_map_validator.py`
- [ ] T013 [P] Unit tests for ghost pathfinding checks in `tests/unit/test_map_validator.py`

---

## Phase 3: User Story 1 - Play Randomly Generated Maps (P1)

*Core feature: Generate and play a single randomly generated map*

### 3.1 Map Generation Core

- [ ] T014 [US1] Implement `src/pacman/generators/random_generator.py` with MapGenerator base class
- [ ] T015 [P] [US1] Implement recursive backtracking maze generation algorithm in random_generator.py with deterministic RNG initialization and seed support for reproducible map generation during testing
- [ ] T016 [P] [US1] Create grid representation and initialization in `src/pacman/generators/grid.py`
- [ ] T017 [P] [US1] Implement pellet placement algorithm (distribute across generated corridors)
- [ ] T018 [P] [US1] Implement Pac-Man spawn point placement (central, safe location)
- [ ] T019 [P] [US1] Implement ghost spawn point placement (distributed, accessible)

### 3.2 Validation & Integration

- [ ] T020 [US1] Integrate generation with validation: MapGenerator calls MapValidator before returning map
- [ ] T021 [US1] Create `src/pacman/generators/factory.py` to instantiate map based on config
- [ ] T022 [US1] Modify `src/pacman/levels/level_loader.py` to load generated maps alongside JSON maps
- [ ] T023 [US1] Update `src/pacman/game.py` to accept map source (random/standard) parameter

### 3.3 UI & Menu Integration

- [ ] T024 [US1] Create `src/pacman/ui/splash.py` for splash screen (title display + key wait for Enter/Space)
- [ ] T025 [US1] Create `src/pacman/ui/map_selector.py` for menu choice (Random vs Standard)
- [ ] T026 [US1] Modify `src/pacman/ui/menu.py` to integrate map selection after "New Game" selection
- [ ] T027 [US1] Update game startup flow in `__main__.py`: splash screen → menu → map selector → game

### 3.4 Testing & Acceptance

- [ ] T028 [US1] Unit test: Map generation produces valid grid in `tests/unit/test_map_generator.py`
- [ ] T029 [US1] Unit test: All pellets are reachable from Pac-Man spawn in `tests/unit/test_map_generator.py`
- [ ] T030 [US1] Unit test: Spawn points are non-overlapping and valid in `tests/unit/test_map_generator.py`
- [ ] T031 [US1] Integration test: Random map loads and player can move Pac-Man in `tests/integration/test_map_generation_flow.py`
- [ ] T032 [US1] Integration test: Standard map selection loads hand-crafted level correctly
- [ ] T033 [US1] Acceptance test: Splash screen displays and transitions on Enter/Space key

---

## Phase 4: User Story 2 - Varied Map Layouts and Themes (P2)

*Layout variety and visual themes for replayability*

### 4.1 Configuration & Variation

- [ ] T034 [P] [US2] Implement wall density parameter in MapGenerator (sparse vs dense wall patterns)
- [ ] T035 [P] [US2] Implement pellet distribution parameter in MapGenerator (varied pellet density)
- [ ] T036 [P] [US2] Modify maze generation to respond to density parameters (control corridor width/spacing)
- [ ] T037 [P] [US2] Create layout variation provider to generate 3+ distinct layout patterns per seed

### 4.2 Theme System

- [ ] T038 [US2] Create `src/pacman/themes/theme_manager.py` to manage 2-3 visual themes
- [ ] T039 [US2] Create `src/pacman/themes/standard_theme.py` with standard tileset mapping
- [ ] T040 [US2] Create `src/pacman/themes/green_star_theme.py` with green star tileset (reuse existing assets)
- [ ] T041 [US2] Create `src/pacman/themes/custom_theme.py` template for future custom themes
- [ ] T042 [US2] Implement theme asset mapping as sprite registry (JSON or Python enum) mapping grid tile types (wall, pellet, powerup spawn) to theme-specific asset sprites; test on standard and green_star themes
- [ ] T043 [US2] Integrate theme selection into map generation config

### 4.3 Testing & Validation

- [ ] T044 [P] [US2] Unit test: Layout variation produces 80% unique maps in `tests/unit/test_map_variety.py`
- [ ] T045 [P] [US2] Unit test: Theme application preserves layout validity
- [ ] T046 [US2] Integration test: Generate 10+ maps, verify theme consistency and variety in `tests/integration/test_layout_variety.py`
- [ ] T047 [US2] Acceptance test: Player sees visually distinct maps across multiple games

---

## Phase 5: User Story 3 - Maps Guarantee Balanced Gameplay (P3)

*Difficulty scaling and playability assurance*

### 5.1 Difficulty & Balancing

- [ ] T048 [P] [US3] Implement difficulty parameter in MapGenerator (maps adjust based on difficulty level)
- [ ] T049 [P] [US3] Implement ghost spawn count scaling based on difficulty (easy: fewer ghosts, hard: more)
- [ ] T050 [P] [US3] Implement ghost AI behavior adjustment per difficulty (speed, chase patterns)
- [ ] T051 [US3] Create `src/pacman/generators/difficulty_adjuster.py` for difficulty-aware generation

### 5.2 Victory Condition & Configuration

- [ ] T052 [US3] Implement victory percentage parameter (default 100%, configurable 80-100%)
- [ ] T053 [US3] Modify game victory check to use configured pellet percentage instead of 100%
- [ ] T054 [US3] Update HUD to display victory percentage target (e.g., "Collect 80% of pellets to win")

### 5.3 Validation & Balance

- [ ] T055 [P] [US3] Implement ghost navigation viability scoring in validator (test all ghost spawns can reach diverse map areas)
- [ ] T056 [P] [US3] Add dead-end trap detection to validator (prevent unreachable pellet pockets)
- [ ] T057 [US3] Create balance test suite in `tests/integration/test_map_balance.py`
- [ ] T058 [US3] Unit test: Ghost AI can navigate 95%+ of generated maps without getting stuck
- [ ] T059 [US3] Unit test: Victory condition scales correctly with configured percentage
- [ ] T060 [US3] Integration test: Run automated games on generated maps, verify 90% completion rate

---

## Phase 6: Failure Handling, Optimization & Polish

*Robustness, performance, and end-to-end validation*

### 6.1 Generation Failure Handling

- [ ] T061 [P] Implement generation timeout logic (3-second limit) in `src/pacman/generators/factory.py`
- [ ] T062 [P] Implement retry mechanism: on timeout, retry with simplified parameters (smaller map, lower density)
- [ ] T063 [P] Implement fallback mechanism: select random vetted level from fallback pool on persistent failure
- [ ] T064 Implement player notification: display message if fallback level is loaded
- [ ] T065 Create `src/pacman/generators/error_handler.py` for generation error recovery

### 6.2 Performance Optimization

- [ ] T066 [P] Optimize maze generation algorithm to achieve <1 second target on medium maps
- [ ] T067 [P] Profile generation and validation (add instrumentation in `src/pacman/generators/profiler.py`)
- [ ] T068 Performance test: Verify 1000+ map generations complete within 1-3 second budget
- [ ] T069 Memory test: Verify no memory leaks during repeated map generation and unloading

### 6.3 Integration & Cross-Cutting

- [ ] T070 [P] Ensure generated maps work with existing pellet collection system (no breaking changes)
- [ ] T071 [P] Ensure generated maps work with existing powerup system (spawn locations valid)
- [ ] T072 [P] Ensure generated maps work with existing ghost AI (no pathfinding breakage)
- [ ] T073 [P] Ensure generated maps work with existing scoring system (pellet/powerup rewards)
- [ ] T074 [P] Ensure generated maps respect existing lives/game-over logic
- [ ] T075 [P] Integration test: End-to-end game flow with random map from splash screen to victory

### 6.4 Code Quality & Documentation

- [ ] T076 Code review: Ensure generators module follows project conventions
- [ ] T077 Add docstrings to all public classes and functions in generators module
- [ ] T078 Create `specs/002-random-map-generation/quickstart.md` with usage examples
- [ ] T079 Update `IMPLEMENTATION_SUMMARY.md` (document design decisions from this feature)
- [ ] T080 Refactor shared utilities into `src/pacman/generators/utils.py` if needed

### 6.5 Final Acceptance

- [ ] T081 [P] Acceptance test: All 3 user stories independently pass acceptance criteria
- [ ] T082 Acceptance test: Splash screen displays on launch, menu works, random/standard both playable
- [ ] T083 Acceptance test: 100% of maps validated for playability before display (SC-002)
- [ ] T084 Acceptance test: 80%+ of generated maps have unique layouts (SC-003)
- [ ] T085 Acceptance test: Ghost AI navigates 95%+ of maps without failure (SC-005)

---

## Dependencies & Execution Strategy

### Task Dependency Graph

```
Setup (T001-T005)
    ↓
Foundational (T006-T013) — blocks all user stories
    ├→ US1 Core Gen (T014-T033) — can execute in parallel with other user stories
    ├→ US2 Variety (T034-T047) — depends on US1 core
    └→ US3 Balance (T048-T060) — depends on US1 core
        ↓
Polish & Optimization (T061-T085) — executes after user stories
```

### Parallel Execution Examples

**For User Story 1 (P1):**
- T015-T019 can run in parallel (independent generation sub-algorithms)
- T024-T026 (UI tasks) can run in parallel with T014-T023 (generation logic)

**For User Story 2 (P2):**
- T034-T036 (density/distribution) and T038-T043 (themes) can run in parallel

**For User Story 3 (P3):**
- T048-T051 (difficulty) and T052-T054 (victory condition) can run in parallel

### Implementation Sequence (MVP First)

1. **Phase 1** (T001-T005): Initialize project structure
2. **Phase 2** (T006-T013): Implement validation (gates all features)
3. **Phase 3** (T014-T033): Complete User Story 1 (playable random maps) — **MVP**
4. **Phase 4** (T034-T047): Add User Story 2 (layout variety)
5. **Phase 5** (T048-T060): Add User Story 3 (balance)
6. **Phase 6** (T061-T085): Optimize, test, polish

---

## Success Criteria Mapping

| Success Criteria | Tasks | Test |
|---|---|---|
| SC-001: Generate map in <2s | T066-T068 | Performance test T068 |
| SC-002: 100% maps validated | T009, T020-T021, T055-T056 | Integration T075 |
| SC-003: 80% unique layouts | T034-T037 | Unit T044 |
| SC-004: 90% completion rate | T048-T060 | Integration T060 |
| SC-005: 95% ghost navigation | T008, T055-T058 | Unit T058 |
| SC-006: Layout consistency | T034-T043 | Integration T046 |

---

## Checklist Format Reference

All tasks follow the strict format:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

- **[P]** = Parallelizable task (can run independently)
- **[Story]** = [US1], [US2], [US3] for user story tasks; omitted for setup/foundational/polish
- **TaskID** = Sequential T001-T085
- **File Path** = Exact source file or test affected
