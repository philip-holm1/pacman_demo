# Implementation Plan: Random Map Generation and Playable Levels

**Branch**: `002-random-map-generation` | **Date**: February 9, 2026 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/002-random-map-generation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enable players to experience procedurally generated Pac-Man maps with guaranteed playability. The system generates grid-based maps (12x12, 16x16, 20x20) meeting core playability constraints (reachable pellets, ghost navigation viability) within 1-3 seconds, with fallback to hand-crafted levels on timeout. Players select between "Random Map" and "Standard Map" at game start. Success depends on deterministic generation, efficient validation (connectivity/pathfinding checks), and composition with existing game mechanics.

## Technical Context

**Language/Version**: Python 3.11+ (existing project baseline)  
**Primary Dependencies**: Procedural generation algorithms (maze/maze-derivative), pathfinding library (BFS/DFS for reachability validation), existing game systems (collision, scoring, ghost AI)  
**Storage**: JSON-based (local level files in `levels/` directory; no database)  
**Testing**: pytest (existing test infrastructure); unit tests for generation + validation; integration tests for end-to-end map load/play  
**Target Platform**: Local single-player desktop game (60 FPS target per constitution)  
**Project Type**: Single project (existing Pac-Man demo structure)  
**Performance Goals**: Map generation within 1-3 seconds (target <1s); validation <100ms per map  
**Constraints**: Deterministic (seeded RNG), grid-based (1 tile = 1 movement unit), 100% playability validation before display, no external dependencies  
**Scale/Scope**: 3 map sizes, 2-3 visual themes, up to 80% layout variety across generated maps

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Mapping to Constitution Requirements:**

| Requirement | Feature Compliance | Status |
|-------------|-------------------|--------|
| Single-player, local gameplay | Supports local random + standard maps; no multiplayer | ✅ Pass |
| Deterministic behavior | Spec requires seeded RNG for reproducibility | ✅ Pass |
| Minimal dependencies | Uses existing game systems only; no external services | ✅ Pass |
| Testable units | Generation validation (connectivity, ghost pathfinding testable) | ✅ Pass |
| Keyboard input | Respects existing controls; menu navigation via keyboard | ✅ Pass |
| 60/30 FPS performance | Generation happens off-screen; 100% validation < 100ms | ✅ Pass |
| Level management | Extends existing `levels/` structure with generated levels | ✅ Pass |
| Persistence | No new persistence required (maps generated fresh each session) | ✅ Pass |
| Local-first | All generation, validation, storage local to game instance | ✅ Pass |

**Violations**: None identified. Feature aligns with constitution constraints.

## Project Structure

### Documentation (this feature)

```text
specs/002-random-map-generation/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (TBD: generation algorithms, validation strategies)
├── data-model.md        # Phase 1 output (TBD: map entity schema, config structure)
├── quickstart.md        # Phase 1 output (TBD: usage examples, API reference)
├── contracts/           # Phase 1 output (TBD: JSON schemas)
└── checklists/
    └── requirements.md  # Quality validation
```

### Source Code (repository root)

```text
src/pacman/
├── generators/                    # NEW: Map generation subsystem
│   ├── __init__.py
│   ├── random_generator.py        # Core generation algorithm
│   ├── validator.py               # Playability validation (connectivity, pathfinding)
│   └── config.py                  # Generation parameters (size, density, pellet distribution)
│
├── levels/                        # EXTENDED: Supports generated + hand-crafted maps
│   ├── level_loader.py            # MODIFIED: Detect/load generated vs standard maps
│   └── schema.py                  # MODIFIED: Validate map structure (existing)
│
├── ui/                            # NEW/EXTENDED: Menu UI for map selection
│   ├── menu.py                    # MODIFIED: Add map selection screen (Random vs Standard)
│   ├── splash.py                  # NEW: Splash screen display + key wait
│   └── screens.py                 # MODIFIED: Handle fallback notification (if gen fails)
│
└── game.py                        # MODIFIED: Initialize with map source (random/standard)

levels/                            # Data directory
├── level1.json                    # Existing hand-crafted level
├── generated/                     # NEW: Runtime-generated levels stored/cached if needed
│   └── (maps generated fresh each game)
└── fallback/                      # NEW: Vetted hand-crafted fallback levels

tests/unit/
├── test_map_generator.py          # NEW: Unit tests for generation algorithm
├── test_map_validator.py          # NEW: Unit tests for validation logic
├── test_map_loader.py             # MODIFIED: Integration with level loader
└── ... existing tests ...

tests/integration/
├── test_map_generation_flow.py    # NEW: E2E flow (menu selection → map load → playable)
└── ... existing tests ...
```

**Structure Decision**: Extend existing single-project structure with a dedicated `src/pacman/generators/` module for generation/validation logic. UI modifications are minimal (add splash screen, map selection menu). Existing level loading infrastructure reused. This minimizes impact on existing systems while keeping generation self-contained and testable.

## Implementation Phases

### Phase 0: Research & Clarification
**Deliverable**: `research.md`

**Research Tracks:**

1. **Procedural Generation Algorithm Selection**
   - Evaluate maze generation approaches: recursive backtracking, Prims, binary space partition (BSP), cellular automata
   - Goal: Deterministic, fast (<1s), variety guarantee, balanceable difficulty
   - Output: Selected algorithm + rationale + pseudocode sketch

2. **Playability Validation Strategy**
   - Connectivity check: flood-fill/BFS from Pac-Man start to ensure all pellets reachable
   - Ghost pathfinding viability: verify ghost AI (existing) can navigate without permanent traps
   - Goal: <100ms validation per map
   - Output: Validation algorithm + performance analysis

3. **Theme/Visual Variation Integration**
   - How to apply 2-3 themes to generated layouts without duplicating generation logic
   - Investigate theme asset mapping (tile sprite selection per theme)
   - Output: Theme application pattern

4. **Fallback Level Pool**
   - Identify which hand-crafted levels can serve as fallbacks (existing level1.json + others)
   - Test ghost AI compatibility on each candidate
   - Output: List of vetted fallback levels + compatibility notes

5. **Existing Game Integration Points**
   - Map how generated maps compose with existing pellet system, ghost AI, scoring, lives
   - Verify no breaking changes needed
   - Output: Integration checklist + modifications scope

### Phase 1: Design & Contracts
**Deliverables**: `data-model.md`, `contracts/`, `quickstart.md`, agent context update

**1a. Data Model** (`data-model.md`)

Define:
- `GeneratedMap` entity: grid layout, spawn points, pellet positions, validated state
- `MapConfig`: size preset (small/medium/large), wall density, pellet density, theme selection, victory percentage
- `MapValidator` result: connectivity check result, ghost pathfinding viability score, validation timestamp
- Relationship to existing `Level` entity

**1b. API Contracts** (`contracts/`)

Define:
- `MapGenerator.generate(config: MapConfig) -> GeneratedMap` — deterministic, seeded RNG
- `MapValidator.validate(map: GeneratedMap) -> ValidationResult` — returns playability metrics
- `MapSelector.select_map() -> MapSource` (RANDOM | STANDARD) — returns choice + selected map
- `LevelLoader.load(map_source: MapSource) -> Level` — MODIFIED to handle generation

JSON schema example:
```json
{
  "mapConfig": {
    "size": "medium",        // small | medium | large
    "wallDensity": 0.35,     // 0.0-1.0 sparse to dense
    "pelletDensity": 0.8,    // 0.0-1.0
    "theme": "standard",     // standard | green_star | custom
    "victoryPercentage": 100 // 80-100
  },
  "generatedMap": {
    "grid": [[...]],         // 2D array, 0=empty, 1=wall, 2=pellet spawn, etc.
    "ghostSpawns": [[x,y]],
    "pacmanSpawn": [x,y],
    "width": 16,
    "height": 16,
    "validatedAt": "2026-02-09T12:00:00Z",
    "validationScore": { "connectivity": 1.0, "ghostPathfinding": 0.98 }
  }
}
```

**1c. Quickstart** (`quickstart.md`)

Provide:
- How to trigger random map generation (code example)
- How to configure map parameters (size, density, theme)
- How to run validation checks
- Example: Playing a generated map vs. standard map

**1d. Agent Context Update**

Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType copilot` to add:
- File structure changes
- New generator module overview
- Key classes and functions to be implemented

### Phase 2: Implementation (Post-Planning)
**Not covered by `/speckit.plan`; use `/speckit.tasks` to generate**

Will include:
- Implement generation algorithm in `src/pacman/generators/random_generator.py`
- Implement validation in `src/pacman/generators/validator.py`
- Integrate menu UI (splash screen, map selection)
- Write unit + integration tests
- Update level loader and game initialization
- Acceptance testing against success criteria

## Complexity Tracking

**Justification**: No constitution violations. Feature scope is bounded and integrates incrementally with existing systems.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
