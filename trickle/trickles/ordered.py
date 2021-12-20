from typing import Any, List, NamedTuple

from trickle.trickles.puddle import Puddle, T
from trickle.trickles.trickle import Path


class Ordered(Puddle[List[T]]):
    # TODO: a lot of this class is highly inefficient and could be sped up with some
    #       smart caching and passing of values in events

    class Index(NamedTuple):
        index: int
        event: Any

    class Added(NamedTuple):
        pass

    class Removed(NamedTuple):
        index: int

    def __init__(self, *puddles: Puddle):
        super().__init__()

        self.puddles = []

        for puddle in puddles:
            # Any events broadcast during this stage will be ignored as the ordered
            # puddle does not yet have any outputs
            self.add(puddle)

    def respond(self, path: Path, event: Any):
        (index,) = path
        assert isinstance(index, int)

        self.broadcast(Ordered.Index(index, event))

    def value(self) -> T:
        return [puddle.value() for puddle in self.puddles]

    def add(self, puddle: Puddle):
        self.listen((len(self.puddles),), puddle)
        self.puddles.append(puddle)
        self.broadcast(Ordered.Added())

    def remove(self, index: int):
        self.ignore((index,))
        del self.puddles[index]
        self.broadcast(Ordered.Removed(index))
