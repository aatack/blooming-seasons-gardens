from typing import Any, Callable, List, NamedTuple, Tuple, cast

from trickle.trickles.puddle import Puddle, T
from trickle.trickles.singular import Derived, Pointer
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
        for i in range(index + 1, len(self.puddles)):
            self.reassign((i,), (i - 1,))

        del self.puddles[index]
        self.broadcast(Indexed.Removed(index))

    def __getitem__(self, index: int) -> Puddle:
        return self.puddles[index]


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
                # The puddle can safely be isolated here since it was created during the
                # course of the map operation
                self.puddles[event.index].isolate()

                self.remove(event.index)
        else:
            super().respond(path, event)

    def add(self, puddle: Puddle):
        if self.function_of_puddle:
            super().add(self.function(puddle))
        else:
            super().add(Derived(self.function, puddle))


class Folded(Indexed):
    def __init__(
        self,
        initial: Puddle,
        function: Callable[[Puddle, Puddle], Tuple[Puddle, Puddle]],
        indexed: Indexed,
    ):
        """
        Perform a fold operation over an ordered group of puddles.

        The folding function should take in the current state and the next puddle, and
        should output the updated state as well as the transformed puddle for that
        index.  An initial state must also be given.
        """
        self.initial = initial
        self.function = function
        self.indexed = indexed

        # List of intermediate states at each step
        self.intermediate: List[Puddle] = []

        super().__init__(*self.indexed.puddles)

        self.listen((), self.indexed)

    def respond(self, path: Path, event: Any):
        if path == ():
            if isinstance(event, Indexed.Added):
                self.add(event.puddle)
            if isinstance(event, Indexed.Removed):
                self.remove(event.index)
        else:
            super().respond(path, event)

    def add(self, puddle: Puddle, broadcast: bool = True):
        next_step, next_puddle = self.function(
            self.intermediate[-1] if len(self.intermediate) > 0 else self.initial,
            puddle,
        )

        # This needs to be listened to so we can pass accurate index events to
        # downstream puddles
        self.listen((len(self.puddles),), next_puddle)

        self.intermediate.append(next_step)
        self.puddles.append(next_puddle)

        if broadcast:
            self.broadcast(Indexed.Added(next_puddle))

    def remove(self, index: int):
        for i in range(index, len(self.puddles)):
            self.ignore((i,))

        # This step is required to prevent the no-longer-active puddles from having any
        # impact.  In theory they can safely be isolated here because they were all
        # created during the course of the fold operation
        for puddle in self.puddles[index:] + self.intermediate[index:]:
            puddle.isolate()

        self.puddles = self.puddles[:index]
        self.intermediate = self.intermediate[:index]

        for puddle in self.indexed.puddles[index:]:
            self.add(puddle, broadcast=False)

        self.broadcast(Indexed.Removed(index))

    def internal_state(self) -> Puddle:
        """Get a puddle that tracks the last value in the internal state."""
        return Pointer(
            lambda f: cast(Folded, f).intermediate[-1]
            if len(cast(Folded, f).intermediate) > 0
            else self.initial,
            self,
        )
