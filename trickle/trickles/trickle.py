import abc
from typing import Any, Dict, Set

Path = tuple


class Trickle(abc.ABC):
    def __init__(self):
        self.input_map: Dict[Path, Trickle] = {}
        self.output_map: Dict[Trickle, Set[Path]] = {}

    @abc.abstractmethod
    def respond(self, path: Path, event: Any):
        """Respond to an event from one of of the listened trickles."""

    def broadcast(self, event: Any):
        """Broadcast an event to any trickle listening to this one."""
        for trickle, paths in self.output_map.items():
            for path in paths:
                trickle.respond(path, event)

    def listen(self, path: Path, trickle: "Trickle"):
        """Listen for events broadcast from a particular trickle."""
        assert path not in self.input_map
        self.input_map[path] = trickle

        if self not in trickle.output_map:
            trickle.output_map[self] = []
        trickle.output_map[self].add(path)

    def ignore(self, path: Path):
        """Ignore events broadcast from a currently listened trickle."""
        trickle = self.input_map.pop(path)

        trickle.output_map[self].remove(path)
        if len(trickle.output_map[self]) == 0:
            del trickle.output_map[self]

