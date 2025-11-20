from __future__ import annotations
from collections import deque
from typing import Deque


class PerfTracker:
    """Tracks recent frame durations to compute an average FPS and max frame time."""

    def __init__(self, max_samples: int = 180) -> None:
        self.samples: Deque[float] = deque(maxlen=max_samples)
        self.accum: float = 0.0
        self.frames: int = 0

    def record_frame(self, dt: float) -> None:
        self.samples.append(dt)
        self.accum += dt
        self.frames += 1

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

    def reset(self) -> None:
        self.samples.clear()
        self.accum = 0.0
        self.frames = 0
