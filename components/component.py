import abc
from typing import Callable, Optional

from trickle import Environment, Puddle, Visual


class Component(abc.ABC):
    def __init__(self):
        self._visual: Optional[Puddle] = None
        self._environment: Optional[Environment] = None

    @abc.abstractmethod
    def construct(self, environment: Environment):
        """
        Construct and return a visual and its (potentially modified) environment.
        
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
        self.construct(environment)
        self.assert_initialised()

        return self._visual

    def assert_initialised(self):
        assert isinstance(
            self._visual, Puddle
        ), "Component's visual was not set during construction"
        assert isinstance(
            self._environment, Environment
        ), "Component's environment was not set during construction"

    @property
    def width(self) -> Puddle[float]:
        self.assert_initialised()
        return self._environment.screen.width

    @property
    def height(self) -> Puddle[float]:
        self.assert_initialised()
        return self._environment.screen.height


class Anonymous(Component):
    def __init__(self, function: Callable[[Environment], Puddle[Visual]]):
        super().__init__()

        self._function = function

    def construct(self, environment: Environment):
        self._visual = self._function(environment)
        self._environment = environment

    def deconstruct(self):
        pass
