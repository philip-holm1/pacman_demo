import random
from typing import List, Optional
from .. import config
from ..entities.powerup import Powerup, PowerupInstance, POWERUP_TYPES
from .game_state import GameState
from . import ghost_ai

class PowerupManager:
    def __init__(self, seed: int = 42) -> None:
        random.seed(seed)
        self.definitions = {
            "SpeedBoost": Powerup(id="SpeedBoost", type="SpeedBoost", duration_seconds=config.DEFAULT_POWERUP_DURATION, value=1.5),
            "GhostFreeze": Powerup(id="GhostFreeze", type="GhostFreeze", duration_seconds=config.DEFAULT_POWERUP_DURATION),
            "ScoreMultiplier": Powerup(id="ScoreMultiplier", type="ScoreMultiplier", duration_seconds=config.DEFAULT_POWERUP_DURATION, value=2),
            "InvincibilityBlink": Powerup(id="InvincibilityBlink", type="InvincibilityBlink", duration_seconds=config.DEFAULT_POWERUP_DURATION),
        }
        self.spawn_retry_limit = 10
        self.next_spawn_at = config.POWERUP_PELLET_THRESHOLD
        self._last_spawn_index: int = 0  # T093 deterministic ordered selection

    # --- Helper methods ---
    def _remaining_ticks(self, inst: PowerupInstance, gs: GameState) -> int:
        return max(0, inst.expires_at_tick - gs.tick_count)

    def _apply_effects(self, gs: GameState) -> None:
        # compute score multiplier
        multiplier_instances = [p for p in gs.player.active_powerups if p.type == "ScoreMultiplier"]
        n = len(multiplier_instances)
        gs.player.score_multiplier = min(2 ** n, config.MAX_SCORE_MULTIPLIER) if n else 1
        speed_inst = next((p for p in gs.player.active_powerups if p.type == "SpeedBoost"), None)
        gs.player.speed_multiplier = 1.5 if speed_inst else 1.0
        freeze_inst = next((p for p in gs.player.active_powerups if p.type == "GhostFreeze"), None)
        for g in gs.ghosts:
            g.state = "frozen" if freeze_inst else "normal"
        inv_inst = next((p for p in gs.player.active_powerups if p.type == "InvincibilityBlink"), None)
        if inv_inst:
            interval_ticks = max(1, int(0.2 * config.TICKS_PER_SECOND))
            if gs.tick_count % interval_ticks == 0:
                gs.player.blink_on = not gs.player.blink_on
        else:
            gs.player.blink_on = True

    def _expire_powerups(self, gs: GameState) -> None:
        before = len(gs.player.active_powerups)
        gs.player.active_powerups = [p for p in gs.player.active_powerups if p.expires_at_tick > gs.tick_count]
        expired = before - len(gs.player.active_powerups)
        if expired:
            gs.event_bus.emit("PowerupExpired", expired_count=expired, tick=gs.tick_count)

    def _ordered_floor_candidates(self, gs: GameState) -> list[tuple[int, int]]:
        tiles: list[tuple[int, int]] = []
        for y in range(1, gs.level.height - 1):
            for x in range(1, gs.level.width - 1):
                if gs.level.is_wall(x, y):
                    continue
                if any(p["x"] == x and p["y"] == y for p in gs.level.pellet_positions):
                    continue
                if any(p["x"] == x and p["y"] == y for p in gs.level.spawned_powerups):
                    continue
                if (gs.player.x == x and gs.player.y == y) or any(g.x == x and g.y == y for g in gs.ghosts):
                    continue
                tiles.append((x, y))
        # Deterministic ordering by row-major (y,x)
        tiles.sort(key=lambda t: (t[1], t[0]))
        return tiles

    def spawn_powerup(self, gs: GameState, powerup_type: str | None = None) -> Optional[Powerup]:
        if powerup_type is None:
            powerup_type = random.choice(list(POWERUP_TYPES))
        definition = self.definitions[powerup_type]
        candidates = self._ordered_floor_candidates(gs)
        if not candidates:
            return None
        # Select deterministically cycling through ordered list
        attempts = 0
        while attempts < self.spawn_retry_limit and candidates:
            idx = self._last_spawn_index % len(candidates)
            x, y = candidates[idx]
            self._last_spawn_index += 1
            # place in spawned_powerups list, not pellet_positions
            gs.level.spawned_powerups.append({"x": x, "y": y, "type": powerup_type})
            gs.event_bus.emit("PowerupSpawned", powerup_type=powerup_type, x=x, y=y)
            return definition
        return None

    def collect_powerup(self, gs: GameState) -> Optional[PowerupInstance]:
        # Check if player is on a spawned powerup tile
        for i, pos in enumerate(list(gs.level.spawned_powerups)):
            if pos["x"] == gs.player.x and pos["y"] == gs.player.y:
                # Use stored powerup type, with test override support
                if getattr(gs, "_force_type", None):
                    powerup_type = gs._force_type  # type: ignore
                elif getattr(gs, "_force_multiplier", False):
                    powerup_type = "ScoreMultiplier"
                else:
                    powerup_type = pos.get("type", "SpeedBoost")
                definition = self.definitions[powerup_type]
                start = gs.tick_count
                expires = start + int(definition.duration_seconds * config.TICKS_PER_SECOND)
                inst = PowerupInstance(powerup_id=definition.id, type=definition.type, start_tick=start, expires_at_tick=expires)
                if inst.type == "ScoreMultiplier":
                    gs.player.active_powerups.append(inst)
                else:
                    replaced = False
                    for existing in gs.player.active_powerups:
                        if existing.type == inst.type:
                            existing.start_tick = start
                            existing.expires_at_tick = expires
                            replaced = True
                            break
                    if not replaced:
                        gs.player.active_powerups.append(inst)
                if inst.type == "InvincibilityBlink":
                    ghost_ai.trigger_frightened(gs)
                # remove collected powerup
                del gs.level.spawned_powerups[i]
                gs.event_bus.emit("PowerupCollected", powerup_type=inst.type, start_tick=start, expires_at_tick=expires)
                return inst
        return None

    def update_powerups(self, gs: GameState) -> None:
        self._expire_powerups(gs)
        self._apply_effects(gs)
        if gs.consumed_pellets >= self.next_spawn_at:
            self.spawn_powerup(gs)
            self.next_spawn_at += config.POWERUP_PELLET_THRESHOLD

powerup_manager = PowerupManager()
