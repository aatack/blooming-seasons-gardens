import abc
from typing import Any, Generic, TypeVar

from trickle.trickles.trickle import Trickle

T = TypeVar("T")


class Puddle(Trickle, Generic[T]):
    """
    Trickle which tracks a state and broadcasts an event whenever that state changes.
    """

    @abc.abstractmethod
    def value(self) -> T:
        """Return the current value being stored in the puddle."""

    def __add__(self, other: Any) -> "Puddle":
        from trickle.trickles.singular import Constant, Derived

        other = other if isinstance(other, Puddle) else Constant(other)
        return Derived(lambda a, b: a + b, self, other)

    def __radd__(self, other: Any) -> "Puddle":
        from trickle.trickles.singular import Constant, Derived

        other = other if isinstance(other, Puddle) else Constant(other)
        return Derived(lambda a, b: b + a, self, other)
