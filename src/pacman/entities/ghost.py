from dataclasses import dataclass

@dataclass
class Ghost:
    id: str
    x: int
    y: int
    state: str = "normal"  # normal, frightened, frozen
    ai_mode: str = "scatter"  # scatter, chase, random
