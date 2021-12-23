from typing import Any, Callable, Optional

from trickle.trickles.trickle import Path, Trickle


class Log(Trickle):
    """Trickle which prints all events coming through it."""

    def __init__(
        self, name: Optional[str] = None, predicate: Optional[Callable] = None
    ):
        super().__init__()

        self.name = name if name is not None else f"Log_{id(self)}"
        self.predicate = predicate

    def respond(self, path: Path, event: Any):
        if self.predicate is None or self.predicate(path, event):
            print(self.name, path, event)
