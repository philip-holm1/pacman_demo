# contracts/powerup_contract.md

This file documents the internal module contract for the `powerup` system — no network APIs are needed. It describes public functions, events, and expected behaviors.

## Module: `powerup_manager`

Public API (Python)

- `spawn_powerup(level, powerup_type=None) -> Optional[Powerup]`
  - Places a powerup on a valid tile in the given level. If `powerup_type` is None, choose according to spawn rules. Retries up to 10 times before returning None.

- `collect_powerup(game_state, player, tile_position) -> Optional[PowerupInstance]`
  - Handles player collecting a powerup at `tile_position`. Creates a `PowerupInstance`, updates score if applicable, emits `PowerupCollected` event, and returns the instance.

- `update_powerups(game_state, tick) -> None`
  - Called each game tick. Applies active powerup effects (e.g., speed changes), evaluates expirations (based on tick counters), and emits `PowerupExpired` events.

Events (synchronous callbacks or pub/sub hooks)
- `PowerupCollected(player_id, powerup_type, start_tick, expires_at_tick)`
- `PowerupExpired(player_id, powerup_type, expired_tick)`

Invariants & Contracts
- `collect_powerup` MUST refresh duration when same-type powerup already active (except `ScoreMultiplier` stacking behavior — multiply and create independent instances per spec).
- `update_powerups` MUST be deterministic: rely on `tick` and not wall-clock time.
- Spawns MUST avoid collisions with walls and actors; on failure after 10 retries, return None and log a benign warning.

Testing Contracts
- Unit tests must assert that `spawn_powerup` respects retry limits and valid tile placement.
- Tests must assert that `collect_powerup` creates instances with correct `expires_at_tick` and that `update_powerups` removes instances at the correct tick.

