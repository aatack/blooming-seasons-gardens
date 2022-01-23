import abc
from typing import Callable

from trickle import Environment, Puddle, Visual


class Component(abc.ABC):

    # TODO: deconstructor (perhaps rename methods to `construct` and `deconstruct`?)

    @abc.abstractmethod
    def __call__(self, environment: Environment) -> Puddle[Visual]:
        """Construct a visual representation of the given puddle."""
        # TODO: only allow each component to be called once


class Anonymous(Component):
    def __init__(self, function: Callable[[Environment], Puddle[Visual]]):
        self._function = function

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        return self._function(environment)
