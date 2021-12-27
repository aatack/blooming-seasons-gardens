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
        assert isinstance(path, Path)

        assert path not in self.input_map
        self.input_map[path] = trickle

        if self not in trickle.output_map:
            trickle.output_map[self] = set()
        trickle.output_map[self].add(path)

    def ignore(self, path: Path):
        """Ignore events broadcast from a currently listened trickle."""
        assert isinstance(path, Path)

        trickle = self.input_map.pop(path)

        trickle.output_map[self].remove(path)
        if len(trickle.output_map[self]) == 0:
            del trickle.output_map[self]

    def isolate(self):
        """Remove all inputs and outputs."""
        for path in self.input_map.keys():
            self.ignore(path)
        # TODO: do we need to isolate the outputs as well?  In theory a trickle should
        #       only ever disconnect itself, but will the GC still be able to get rid of
        #       trickles that do not have their outputs disconnected?  Should be
        #       possible in theory

    def reassign(self, old_path: Path, new_path: Path):
        """Change the path by which one trickle listens to another."""
        assert new_path not in self.input_map
        trickle = self.input_map.pop(old_path)

        self.input_map[new_path] = trickle

        # Note that because the same trickle can be passed by multiple paths, there is
        # no need for reference counting (or rather, there is, but it's done implicitly)
        trickle.output_map[self].remove(old_path)
        trickle.output_map[self].add(new_path)
