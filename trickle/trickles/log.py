from typing import Any, Optional

from trickle.trickles.trickle import Path, Trickle


class Log(Trickle):
    """Trickle which prints all events coming through it."""

    def __init__(self, name: Optional[str] = None):
        super().__init__()

        self.name = name if name is not None else f"Log_{id(self)}"

    def respond(self, path: Path, event: Any):
        print(self.name, path, event)
