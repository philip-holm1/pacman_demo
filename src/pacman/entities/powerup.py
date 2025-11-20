from dataclasses import dataclass

POWERUP_TYPES = {"SpeedBoost", "GhostFreeze", "ScoreMultiplier", "InvincibilityBlink"}

@dataclass
class Powerup:
    id: str
    type: str
    duration_seconds: float
    value: float | int | None = None

@dataclass
class PowerupInstance:
    powerup_id: str
    type: str
    start_tick: int
    expires_at_tick: int

    def remaining_ticks(self, current_tick: int) -> int:
        return max(0, self.expires_at_tick - current_tick)
