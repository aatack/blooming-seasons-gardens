from typing import Any, Callable, NamedTuple

from trickle.trickles.puddle import Puddle, T
from trickle.trickles.trickle import Path


class Constant(Puddle):
    def __init__(self, constant_value: T):
        super().__init__()

        self.constant_value = constant_value

    def respond(self, path: Path, event: Any):
        raise Exception(
            f"Trickles of type {type(self.__name__)} should never listen to another "
            "trickle"
        )

    def value(self) -> T:
        return self.constant_value


class Variable(Puddle):
    class Changed(NamedTuple):
        old_value: T
        new_value: T

    def __init__(self, initial_value: T):
        super().__init__()

        self.current_value = initial_value

    def respond(self, path: Path, event: Any):
        raise Exception(
            f"Trickles of type {type(self.__name__)} should never listen to another "
            "trickle"
        )

    def value(self) -> T:
        return self.current_value

    def change(self, new_value: T):
        old_value = self.current_value
        self.current_value = new_value

        self.broadcast(Variable.Changed(old_value, new_value))


class Derived(Puddle):
    class Changed(NamedTuple):
        old_value: T
        new_value: T

    def __init__(self, function: Callable, *ordered: Puddle, **keyed: Puddle):
        super().__init__()

        self.function = function
        self.ordered = ordered
        self.keyed = keyed

        self.current_value = self.compute()

        for index, puddle in enumerate(self.ordered):
            self.listen((index,), puddle)
        for key, puddle in self.keyed.items():
            self.listen((key,), puddle)

    def respond(self, path: Path, event: Any):
        old_value = self.current_value

        self.current_value = self.compute()
        self.broadcast(Derived.Changed(old_value, self.current_value))

    def value(self) -> T:
        return self.current_value

    def compute(self) -> T:
        return self.function(
            *[puddle.value() for puddle in self.ordered],
            **{key: puddle.value() for key, puddle in self.keyed.items()},
        )
