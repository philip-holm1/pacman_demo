# research.md — Modern Powerups (Phase 0)

## Purpose
Resolve open technical clarifications from the feature spec and document key design choices and alternatives.

---

### Decision: Language & Library
- Decision: Use **Python 3.11** and **pygame** for rendering/input/audio.
- Rationale: Lightweight, widely available, good for rapid prototyping and desktop local games. `pygame` exposes keyboard events and basic rendering which is sufficient for a retro Pacman demo. A large portion of the game logic can be tested independently of `pygame` by isolating rendering/I-O behind interfaces.
- Alternatives considered:
  - `arcade` (Python): nicer API, hardware-accelerated; slightly higher dependency surface. Rejected for initial speed of development and ecosystem familiarity.
  - Web (HTML5/canvas): broader reach but requires web packaging and different testing; out of scope (constitution: local desktop).

### Decision: Deterministic Loop
- Decision: Implement a fixed-timestep game loop (e.g., 60 updates/sec) with frame interpolation for smooth rendering.
- Rationale: Fixed-timestep ensures deterministic behavior for physics, collision, and powerup timers across runs — important for testing and the constitution.
- Alternatives: Variable timestep with delta-time; simpler but less deterministic. Rejected because determinism is a constitutional requirement.

### Decision: Powerup Behavior
- Decision: Different powerups run concurrently; collecting the same powerup refreshes its duration (no stacking), except `ScoreMultiplier` is allowed to stack multiplicatively per spec (explicit exception in spec). Default duration is configurable (8s).
- Rationale: Matches stakeholder clarifications in `spec_filled.md` and keeps rules simple and testable.
- Alternatives: Queueing or stacking all powerups; rejected because it complicates expected player feedback and testability.

### Decision: Powerup Spawn Logic
- Decision: Spawn powerups only after configurable pellet thresholds/events. Spawn must choose a valid, non-blocked tile; if spawn location invalid, retry up to 10 times then skip this spawn interval.
- Rationale: Matches spec FR-003 and avoids placing pickups inside walls or on actors.
- Alternatives: Random periodic spawn regardless of pellets — rejected per spec.

### Decision: UI Timer
- Decision: Show a small progress bar under each powerup icon in the HUD (progress bar + remaining time tooltip optional).
- Rationale: Chosen in clarifications and keeps HUD unobtrusive while providing clear duration feedback.

### Decision: Audio/Visual Feedback
- Decision: Play a distinct 0.5s retro animation + short sound for each powerup pick-up.
- Rationale: Matches clarified preference and improves feedback.
- Alternatives: Only sound or only animation (less clear feedback); rejected.

### Decision: Persistence
- Decision: Use local JSON file `data/highscore.json` to store high score. If write fails, fall back to in-memory and log warning.
- Rationale: Minimal, cross-platform, easy to implement and inspect.

### Decision: Tests
- Decision: Use `pytest` for unit tests focused on deterministic logic (spawn logic, collision, powerup timers, scoring). Keep `pygame`-dependent code thin and separate so most tests don't require a display or event loop.

---

## Research Tasks (for Phase 0)
- Implement a simple fixed-timestep loop prototype to validate timing behavior with `pygame`.
- Prototype powerup manager data-structures and timer refresh behavior.
- Validate spawn retry logic on a small sample level map.

---

## Resolved Clarifications (from spec)
- Different powerups run concurrently; collecting same refreshes duration (no stacking), except `ScoreMultiplier` stacking is allowed per spec.
- Powerups spawn after events/pellet thresholds (configurable).
- UI shows progress bar under icon for timers.
- Audio + animation for pickups (0.5s) distinct per type.
- Pause/Resume freezes powerup timers and effects.
- Spawn retry attempts: 10 times, then skip.

---

## Deliverables from Phase 0
- `specs/master/research.md` (this file)
- Clear decisions to feed Phase 1 design artifacts: `data-model.md`, `contracts/`, and `quickstart.md`.

