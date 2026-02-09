# Feature Specification: Green Star Skins

**Feature Branch**: `001-skins-green-star`  
**Created**: December 2, 2025  
**Status**: Draft  
**Input**: User description: "Create a specification for a new feature/skin for the game. The game must support skins for players, ghosts, powerups and pellets. I want to add a skin where the player is a green star and the other objects are something related to that."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Select and play with Green Star skin (Priority: P1)

Players can enable the "Green Star" skin theme and immediately see the player character rendered as a green star with theme-consistent visuals for ghosts, powerups, and pellets.

**Why this priority**: Delivers visible user value fast; validates the skin system end-to-end in normal gameplay.

**Independent Test**: Enable the skin, start level 1, verify all four object categories (player, ghosts, powerups, pellets) adopt theme visuals consistently without affecting mechanics.

**Acceptance Scenarios**:

1. **Given** game settings with "Green Star" skin selected, **When** a new game starts, **Then** the player sprite is a green star and ghosts/powerups/pellets all use matching theme assets.
2. **Given** "Green Star" skin is active, **When** pausing and resuming, **Then** visuals remain themed with no reversion or flicker.

---

### User Story 2 - Skin persists and can be changed (Priority: P2)

Players can switch between the default look and the "Green Star" skin, and the choice persists across sessions.

**Why this priority**: Supports preference management and basic UX continuity.

**Independent Test**: Change skin, restart the game, confirm the skin choice is retained; revert to default and confirm persistence.

**Acceptance Scenarios**:

1. **Given** a player selects "Green Star" skin in Main Menu > Settings > Skin, **When** the game restarts, **Then** the same skin is active without re-selection.
2. **Given** a player switches back to default skin in Settings, **When** the game restarts, **Then** the default visuals are restored.

---

### User Story 3 - Accessibility and clarity (Priority: P3)

The themed visuals remain readable and do not impair gameplay clarity (e.g., collision visibility, frightened mode signals).

**Why this priority**: Avoids UX regressions and ensures theme does not reduce playability.

**Independent Test**: Play a timed session using the skin; verify that feedback states (invincibility blink, frightened ghosts, powerup timers) are distinguishable.

**Acceptance Scenarios**:

1. **Given** the "Green Star" skin is active, **When** a powerup triggers invincibility, **Then** the player's visual feedback (blink/outline) is still apparent.
2. **Given** ghosts enter frightened mode, **When** they are themed, **Then** their frightened state remains visually distinct from normal (e.g., color shift to cyan plus a 2px white outline; contrast ratio ≥ 4.5:1 against maze walls).

---

### Edge Cases

- Skin assets missing: If any themed asset fails to load, fall back to default visuals for that category without crashing.
- Mixed theme state: If settings are partially applied, game should render either fully default or fully themed for each category; avoid mixing within a category.
- Performance on low-spec devices: Themed assets must not degrade frame timing compared to default experience.
- Pause/restart: Skins must remain consistent through pause, level transition, and restart flows.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The game MUST support a skin system that applies visuals for four categories: player, ghosts, powerups, and pellets.
- **FR-002**: A selectable "Green Star" skin MUST render the player as a green star.
- **FR-003**: The "Green Star" skin MUST provide theme-consistent visuals for ghosts, powerups, and pellets.
- **FR-004**: Users MUST be able to select and switch between the default visuals and the "Green Star" skin from the main menu settings; changes apply on the next start of gameplay.
- **FR-010**: The main menu MUST include a "Settings" entry containing a "Skin" selector with preview thumbnails for available skins (at minimum: Default, Green Star).
- **FR-005**: The selected skin MUST persist across game restarts.
- **FR-006**: The skin system MUST not alter gameplay mechanics, timings, collisions, or scoring; visuals only.
- **FR-007**: If a themed asset is unavailable or fails to load, the system MUST gracefully fall back to default visuals for that category.
- **FR-008**: The skin system MUST maintain clarity of gameplay states (e.g., frightened ghosts, invincibility feedback) when themed.
- **FR-009**: The skin system MUST ensure that enabling or disabling a skin does not introduce frame drops beyond acceptable performance criteria.
 - **FR-011**: The "Green Star" skin MUST specify category visuals explicitly: ghosts appear as comet-tail forms (with frightened state visually distinct), powerups appear as star shards, and pellets appear as stardust dots; all assets maintain collision bounds and readability.
 - **FR-012**: Skin assets MUST use PNG spritesheets at 1x/2x resolutions with a 64px base tile size; maximum spritesheet size is 2048x2048; UI previews use scaled raster thumbnails derived from these spritesheets.

### Key Entities *(include if feature involves data)*

- **Skin**: Represents a named visual theme; includes category-specific asset references (player, ghosts, powerups, pellets) and metadata (display name, description).
- **SkinPreference**: Represents the active skin selection per user/session; includes selected skin name and last-updated timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can enable the "Green Star" skin and start playing within 10 seconds from settings to gameplay.
- **SC-002**: With the "Green Star" skin active, 95% of frames render without noticeable visual artifacts or stutter during a 2-minute session.
- **SC-003**: 90% of test players correctly identify frightened ghost state and invincibility feedback within 5 seconds when using the skin.
- **SC-004**: 100% of sessions retain the selected skin after restart when changed via settings.
- **SC-005**: Performance target met: average FPS ≥ 58 and ≥95% of frames render under 16.7ms over a continuous 2-minute session with the skin enabled.

## Assumptions

- Skins affect only visual assets and simple visual effects; no changes to physics or AI.
- A single global skin selection applies to all categories; per-category overrides are out of scope for this feature.
- The "Green Star" theme will include clearly distinguishable variants for special states (e.g., frightened) using color/brightness/outline changes.
- Determinism preserved: collision boxes, update order, timing, and scoring remain unchanged under all skins.

## Clarifications

### Session 2025-12-02

- Q: Define themed visuals per category (ghosts/powerups/pellets)? → A: Ghosts as comet tails, powerups as star shards, pellets as stardust dots
- Q: Define asset resolution and format constraints? → A: PNG spritesheets, 1x/2x (64px base), max 2048x2048

Applied updates:
- Functional Requirements updated to specify selection occurs in main menu and applies on next start of gameplay.
- Interaction & UX Flow updated: Main menu includes Settings; inside Settings, a Skin selector with preview thumbnails (Default, Green Star).
- Themed visuals explicitly defined for each category.
- Asset constraints specified for format and resolutions.
