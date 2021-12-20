from typing import Any, Dict, NamedTuple

from trickle.trickles.puddle import Puddle
from trickle.trickles.trickle import Path


class Keyed(Puddle[Dict[str, Any]]):
    # TODO: a lot of this class is highly inefficient and could be sped up with some
    #       smart caching and passing of values in events

    class Key(NamedTuple):
        key: str
        event: Any

    class Added(NamedTuple):
        key: str

    class Removed(NamedTuple):
        key: str

    def __init__(self, **puddles: Puddle):
        super().__init__()

        self.puddles = {}

        for key, puddle in puddles.items():
            # Any events broadcast during this stage will be ignored as the keyed
            # puddle does not yet have any outputs
            self.add(key, puddle)

    def respond(self, path: Path, event: Any):
        (key,) = path
        assert isinstance(key, str)

        self.broadcast(Keyed.Key(key, event))

    def value(self) -> Any:
        return {key: puddle.value() for key, puddle in self.puddles.items()}

    def add(self, key: str, puddle: Puddle):
        self.listen((key,), puddle)
        self.puddles[key] = puddle
        self.broadcast(Keyed.Added(key))

    def remove(self, key: str):
        self.ignore((key,))
        del self.puddles[key]
        self.broadcast(Keyed.Removed(key))
