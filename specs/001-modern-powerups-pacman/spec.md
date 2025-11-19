# Feature Specification: Modern Powerups — Pacman (Single-player)

**Feature Branch**: `001-modern-powerups-pacman`  
**Created**: 2025-11-19  
**Status**: Draft  
**Input**: User description: "i am creating a pacman game but with a more modern twist. Keep the games retro feel but I want to incorporate something new with different powerups. Its a Single player to be played locally on the device. create the specification for this product"

## Summary

Add a set of modern, varied powerups and related UX polish to a classic single-player Pacman-style game while preserving the retro look-and-feel. Powerups should introduce short-term strategic choices and new player goals without altering core maze and ghost behavior beyond clear, testable effects.

## Goals

- Refresh classic gameplay with new powerup mechanics and pick-ups that feel modern but retro-styled.
- Keep single-player, local-first experience; no online multiplayer required.
- Make additions modular so the core game remains recognizable and playable without powerups.

## Clarifications

### Session 2025-11-19

- Q: Should different powerups run concurrently, replace the active effect, or queue? → A: Option A — Different powerups run concurrently; collecting the same powerup refreshes its duration (no stacking).
 - Q: Target platform and primary input method? → A: Option A — Desktop (Windows/macOS/Linux) — primary input: keyboard; optional gamepad support.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Start & Play (Priority: P1)

As a player, I can start a local game, control Pacman, collect pellets and powerups, and complete a level.

Why this priority: Core loop — without this the feature has no value.

Independent Test: Launch the game, start a level, control player to collect pellets and at least one powerup; level completes when all pellets collected.

Acceptance Scenarios:
1. Given the main menu, When the player starts a new game, Then the first level begins and player control is responsive.
2. Given an active level, When the player collects all pellets, Then the level completes and score/summary is shown.

---

### User Story 2 — Powerup Interaction (Priority: P1)

As a player, I can collect powerups that temporarily modify gameplay (e.g., speed boost, ghost-freeze, score multiplier), and the effect ends after a short, visible duration.

Why this priority: Core new feature requested by stakeholder; must be reliable and testable.

Independent Test: In any level, collect each powerup type and observe deterministic behavior and visible UI indication of remaining duration.

Acceptance Scenarios:
1. Given a powerup is collected, When collected, Then the corresponding effect activates immediately and a timer or UI indicator is shown.
2. Given the powerup effect is active, When the duration expires, Then the effect ends and the UI indicator clears.

---

### User Story 3 — Score & Feedback (Priority: P2)

As a player, I receive immediate visual and audio feedback when picking powerups and scoring; the scoreboard updates accordingly.

Why this priority: Keeps the experience satisfying and testable.

Independent Test: Collect powerups and pellets and verify score increases and on-screen feedback appears (floating points, sound cue).

Acceptance Scenarios:
1. Given a powerup is collected, When collected, Then a short animation and sound play and the score reflects any instant score bonus.

---

### Edge Cases

- Player collects two different powerups in quick succession: different powerups run concurrently; collecting the same powerup refreshes its duration (does not stack).
- Powerup spawn attempts to place an item inside a wall or ghost: game must retry spawn location until valid.
- If the game is paused while a powerup is active, timers pause and resume on unpause.

## Functional Requirements *(mandatory & testable)*

### Powerup System

- **FR-001**: The game MUST support at least four distinct powerup types with deterministic, documented effects: `SpeedBoost`, `GhostFreeze`, `ScoreMultiplier`, and `InvincibilityBlink`.
- **FR-002**: Each powerup MUST have a configurable duration (default 8 seconds) and a visual timer visible to the player.
- **FR-003**: Powerups MUST spawn at predictable intervals (configurable) and only on valid, non-blocked tiles.
- **FR-004**: When a powerup is collected, the effect MUST begin immediately and expire automatically after its duration.
- **FR-005**: The system MUST define stacking rules: collecting the same powerup while active MUST refresh duration (not stack). Different powerup types MUST run concurrently.

### Gameplay & UX

- **FR-006**: UI MUST present an unobtrusive HUD element showing active powerups and remaining time.
- **FR-007**: There MUST be distinct visual and audio feedback for each powerup pickup (retro-styled effects).
- **FR-008**: Pause/Resume MUST pause powerup timers and effects.

### Score & Persistence

- **FR-009**: Score calculation MUST account for active `ScoreMultiplier` powerups deterministically.
- **FR-010**: High score MUST be stored locally on device (simple local persistence) and displayable from the main menu.

### Testing & Stability

- **FR-011**: The game MUST not deadlock or crash if a powerup spawns and a ghost/actor overlaps — spawning must avoid collisions.

## Key Entities

- **Player**: position, velocity, current active powerups (list), score.
- **Powerup**: id, type, spawnLocation, durationSeconds, value (score bonus if any), visualAssetRef.
- **Ghost**: position, state (normal, frightened, frozen), pathfinding mode.
- **Level**: tile grid, pellet locations, powerup spawn points, ghost spawn points.

## Success Criteria *(measurable & verifiable)*

- **SC-001**: A new local player can start and complete a level within 10 seconds of launching the game on a supported device (first-play latency: <10s to start).
- **SC-002**: All four powerup types are collectible and produce the documented effect 100% of the time in 20 representative playthrough tests.
- **SC-003**: Powerup visual timers accurately reflect remaining time within ±0.5s for durations up to 20s in 20 tests.
- **SC-004**: Game does not crash or hang during 1 hour of continuous automated gameplay with randomized spawns.
- **SC-005**: Local high score persists across application restarts in 5 consecutive runs.

## Assumptions

- Single-player local experience only: no online sync or multiplayer.
- Platform details (desktop vs mobile) are not required for this spec; UI and control mapping are expected to be adapted later.
- Art and sound assets will be provided in retro style; placeholder assets allowed for development.

## Out of Scope

- Online leaderboards, cloud saves, multiplayer modes, or community mod tooling.

## Dependencies

- Retro-themed art and sound assets for powerups and HUD.
- QA playtest time for verifying balance and powerup effects.

## Acceptance Criteria (developer-ready)

- AC-001: Branch `001-modern-powerups-pacman` contains the implemented powerup system and UI changes.
- AC-002: Automated test suite includes deterministic tests for spawn logic and timer behavior for the four powerups.
- AC-003: Manual QA checklist demonstrates SC-002 and SC-003 over 20 playthroughs.

## Notes and Next Steps

- After sign-off on this spec, produce a short tech spike to prototype `SpeedBoost` and `GhostFreeze` and a small playtest to verify feel and balance.

---

*End of specification*
