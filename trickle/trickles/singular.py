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
        pass

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
        self.current_value = new_value
        self.broadcast(Variable.Changed())

    def change_as_function(self, function: Callable[[T], T]):
        self.change(function(self.value()))


class Derived(Puddle):
    class Changed(NamedTuple):
        pass

    def __init__(self, function: Callable, *indexed: Puddle, **keyed: Puddle):
        super().__init__()

        self.function = function
        self.indexed = indexed
        self.keyed = keyed

        self.current_value = self.compute()

        for index, puddle in enumerate(self.indexed):
            self.listen((index,), puddle)
        for key, puddle in self.keyed.items():
            self.listen((key,), puddle)

    def respond(self, path: Path, event: Any):
        previous_value = self.current_value
        self.current_value = self.compute()
        if self.current_value != previous_value:
            self.broadcast(Derived.Changed())

    def value(self) -> T:
        return self.current_value

    def compute(self) -> T:
        return self.function(
            *[puddle.value() for puddle in self.indexed],
            **{key: puddle.value() for key, puddle in self.keyed.items()},
        )


class Function(Puddle):
    class Changed(NamedTuple):
        pass

    def __init__(self, function: Callable, *indexed: Puddle, **keyed: Puddle):
        super().__init__()

        self.function = function
        self.indexed = indexed
        self.keyed = keyed

        self.current_value = self.compute()

        for index, puddle in enumerate(self.indexed):
            self.listen((index,), puddle)
        for key, puddle in self.keyed.items():
            self.listen((key,), puddle)

    def respond(self, path: Path, event: Any):
        previous_value = self.current_value
        self.current_value = self.compute()
        if self.current_value != previous_value:
            self.broadcast(Function.Changed())

    def value(self) -> T:
        return self.current_value

    def compute(self) -> T:
        return self.function(
            *[puddle for puddle in self.indexed],
            **{key: puddle for key, puddle in self.keyed.items()},
        )
