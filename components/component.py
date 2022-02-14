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

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        """Construct a visual representation of a component within an environment."""
        assert self._visual is None
        self.construct(environment)

        assert isinstance(self._visual, Puddle)
        return self._visual

    @property
    def top(self) -> Puddle[float]:
        assert isinstance(self._visual, Puddle)
        return Derived(lambda v: v.top(), self._visual)

    @property
    def left(self) -> Puddle[float]:
        assert isinstance(self._visual, Puddle)
        return Derived(lambda v: v.left(), self._visual)

    @property
    def bottom(self) -> Puddle[float]:
        assert isinstance(self._visual, Puddle)
        return Derived(lambda v: v.bottom(), self._visual)

    @property
    def right(self) -> Puddle[float]:
        assert isinstance(self._visual, Puddle)
        return Derived(lambda v: v.right(), self._visual)


class Anonymous(Component):
    def __init__(self, function: Callable[[Environment], Puddle[Visual]]):
        super().__init__()

        self._function = function

    def construct(self, environment: Environment):
        self._visual = self._function(environment)
        self._environment = environment

    def deconstruct(self):
        pass
