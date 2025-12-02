# Implementation Plan: Green Star Skins

**Branch**: `001-skins-green-star` | **Date**: December 2, 2025 | **Spec**: `specs/001-skins-green-star/spec.md`
**Input**: Feature specification from `/specs/001-skins-green-star/spec.md`

## Summary

Add a visual skin system covering player, ghosts, powerups, and pellets, with a selectable "Green Star" theme. Provide main‑menu Settings with a Skin selector and persistence. Assets follow PNG spritesheet constraints (1x/2x, 64px base, max 2048x2048). No gameplay changes.

## Technical Context

**Language/Version**: Python 3.x (repo uses `python -m pacman`)  
**Primary Dependencies**: pygame (to be confirmed in Phase 0), json for config/persistence  
**Storage**: Local files (`data/highscore.json`, `data/settings.json` for skin persistence)  
**Testing**: pytest (tests present under `tests/unit`)  
**Target Platform**: Windows/macOS/Linux desktop (local only)  
**Project Type**: Single local game project (`src/pacman`)  
**Performance Goals**: Maintain current FPS; target 60 FPS; no additional frame drops  
**Constraints**: Offline-only; deterministic behavior unchanged; asset memory within current bounds  
**Scale/Scope**: Single-player; one level (`levels/level1.json`); extend visuals only

Unknowns marked for Phase 0:
- NEEDS CLARIFICATION: Confirm rendering lib (pygame or alternative) and sprite pipeline used.
- NEEDS CLARIFICATION: Current asset loader paths and how to inject skin asset overrides.
- RESOLVED: Persist skin preference in `data/settings.json` (JSON file).

## Constitution Check

Gates based on constitution:
- Local-only: satisfied (no network).  
- Deterministic: visuals only; must not affect gameplay timing or collisions.  
- Testable: add unit checks for selection persistence and asset fallback; avoid changing logic tests.  
- Performance: maintain stable FPS; add a simple timing check if needed.

Gate status: PASS, contingent on enforcing “visuals only” and FPS not degraded.

## Project Structure

### Documentation (this feature)

```text
specs/001-skins-green-star/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md   (created later by /speckit.tasks)
```

### Source Code (repository root)

```text
src/pacman/
├── config.py            # add skin preference key (persisted setting)
├── game.py              # load skin preference; pass theme to rendering
├── entities/
│   ├── player.py        # apply player sprite override (green star)
│   ├── ghost.py         # apply comet-tail visuals; frightened variant
│   └── powerup.py       # apply star shard visuals
├── systems/             # if rendering systems exist, inject skin assets
└── assets/              # under repo root: assets/sprites/skins/green_star/*

tests/unit/
├── test_skin_selection_persistence.py   # new
├── test_skin_asset_fallbacks.py         # new
├── test_skin_settings_preview.py       # new
└── test_visuals_only_behavior.py       # new (assert collisions/timing unchanged with skin)
```

**Structure Decision**: Single local game project. Add a `assets/sprites/skins/green_star/` subtree and minimal config hook in `config.py`. Keep changes surgical to preserve existing behavior and tests.

## Complexity Tracking

No constitution violations anticipated. If asset injection requires a loader refactor, document why and keep it minimal.
