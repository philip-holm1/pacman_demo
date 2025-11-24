from __future__ import annotations
from collections import deque
from typing import Deque


class PerfTracker:
    """Tracks frame and logic tick durations (T092).

    Frame durations measure render/update loop accumulation; tick durations
    measure time spent executing one game logic tick.
    """

    def __init__(self, max_samples: int = 180) -> None:
        self.samples: Deque[float] = deque(maxlen=max_samples)
        self.tick_samples: Deque[float] = deque(maxlen=max_samples)
        self.accum: float = 0.0
        self.frames: int = 0
        self.ticks: int = 0

    def record_frame(self, dt: float) -> None:
        self.samples.append(dt)
        self.accum += dt
        self.frames += 1

    def record_tick(self, dt: float) -> None:
        self.tick_samples.append(dt)
        self.ticks += 1

    def avg_fps(self) -> float:
        if not self.samples:
            return 0.0
        total = sum(self.samples)
        if total <= 0:
            return 0.0
        return len(self.samples) / total

    def worst_ms(self) -> float:
        if not self.samples:
            return 0.0
        return max(self.samples) * 1000.0

    def avg_tick_ms(self) -> float:
        if not self.tick_samples:
            return 0.0
        return (sum(self.tick_samples) / len(self.tick_samples)) * 1000.0

    def worst_tick_ms(self) -> float:
        if not self.tick_samples:
            return 0.0
        return max(self.tick_samples) * 1000.0

    def reset(self) -> None:
        self.samples.clear()
        self.tick_samples.clear()
        self.accum = 0.0
        self.frames = 0
        self.ticks = 0
