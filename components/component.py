import abc

from trickle import Environment, Puddle, Visual


class Component(abc.ABC):
    @abc.abstractmethod
    def __call__(self, environment: Environment) -> Puddle[Visual]:
        """Construct a visual representation of the given puddle."""
