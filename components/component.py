import abc
from typing import Callable, Optional

from trickle import Environment, Puddle, Visual
from trickle.trickles.interaction import Screen
from trickle.trickles.singular import Derived


class Component(abc.ABC):
    def __init__(self):
        self._visual: Optional[Puddle] = None

    @abc.abstractmethod
    def construct(self, environment: Environment):
        """
        Construct a visual for the component and store it internally.
        
        The visual and environment should be saved to `self._visual` and
        `self._environment` respectively; an error will be thrown if either is left as
        `None`.
        """

    @abc.abstractmethod
    def deconstruct(self):
        """
        Do any work necessary to ensure the component's puddles are garbage collected.
        """

    @abc.abstractmethod
    def _width(self) -> Puddle[float]:
        """Return  a puddle denoting the width of the constructed component."""

    @abc.abstractmethod
    def _height(self) -> Puddle[float]:
        """Return  a puddle denoting the height of the constructed component."""

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        """Construct a visual representation of a component within an environment."""
        assert self._visual is None
        self.construct(environment)

        assert isinstance(self._visual, Puddle)
        return self._visual

    @property
    def width(self) -> Puddle[float]:
        # TODO: cache the result and lower bound it at zero
        return self._width()

    @property
    def height(self) -> Puddle[float]:
        # TODO: cache the result and lower bound it at zero
        return self._height()


class Anonymous(Component):
    def __init__(self, function: Callable[[Environment], Puddle[Visual]]):
        super().__init__()

        self._function = function

    def construct(self, environment: Environment):
        self._visual = self._function(environment)
        self._environment = environment

    def deconstruct(self):
        pass

    def _width(self) -> Puddle[float]:
        return Derived(lambda v: v.right(), self._visual)

    def _height(self) -> Puddle[float]:
        return Derived(lambda v: v.bottom(), self._visual)
