from collections import defaultdict
from typing import Callable, Dict, List, Any

class EventBus:
    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable[..., None]]] = defaultdict(list)

    def subscribe(self, event: str, cb: Callable[..., None]) -> None:
        self._subs[event].append(cb)

    def emit(self, event: str, **payload: Any) -> None:
        for cb in self._subs.get(event, []):
            cb(**payload)
