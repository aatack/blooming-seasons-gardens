from typing import Any, Callable, List, NamedTuple

from trickle.trickles.puddle import Puddle, T
from trickle.trickles.singular import Derived
from trickle.trickles.trickle import Path


class Indexed(Puddle[List[T]]):
    # TODO: a lot of this class is highly inefficient and could be sped up with some
    #       smart caching and passing of values in events

    class Index(NamedTuple):
        index: int
        event: Any

    class Added(NamedTuple):
        puddle: Puddle

    class Removed(NamedTuple):
        index: int

    def __init__(self, *puddles: Puddle):
        super().__init__()

        self.puddles = []

        for puddle in puddles:
            # Any events broadcast during this stage will be ignored as the indexed
            # puddle does not yet have any outputs
            self.add(puddle)

    def respond(self, path: Path, event: Any):
        (index,) = path
        assert isinstance(index, int)

        self.broadcast(Indexed.Index(index, event))

    def value(self) -> T:
        return [puddle.value() for puddle in self.puddles]

    def add(self, puddle: Puddle):
        self.listen((len(self.puddles),), puddle)
        self.puddles.append(puddle)
        self.broadcast(Indexed.Added(puddle))

    def remove(self, index: int):
        self.ignore((index,))
        del self.puddles[index]
        self.broadcast(Indexed.Removed(index))


class Mapped(Indexed):
    def __init__(
        self, function: Callable, indexed: Indexed, function_of_puddle: bool = False,
    ):
        self.function = function
        self.indexed = indexed
        self.function_of_puddle = function_of_puddle

        super().__init__(*self.indexed.puddles)

        self.listen((), self.indexed)

        # NOTE: problems may be caused if the add or remove functions are ever called
        #       manually; would be good to investigate a way to avoid this from
        #       happening while also allowing the inherited methods to be used in the
        #       constructor

    def respond(self, path: Path, event: Any):
        if path == ():
            if isinstance(event, Indexed.Added):
                self.add(event.puddle)
            if isinstance(event, Indexed.Removed):
                self.remove(event.index)
        else:
            super().respond(path, event)

    def add(self, puddle: Puddle):
        if self.function_of_puddle:
            super().add(self.function(puddle))
        else:
            super().add(Derived(self.function, puddle))
