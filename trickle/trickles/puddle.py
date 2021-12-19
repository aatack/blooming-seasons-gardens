import abc
from typing import Generic, TypeVar

from trickle.trickles.trickle import Trickle

T = TypeVar("T")


class Puddle(Trickle, Generic[T]):
    """
    Trickle which tracks a state and broadcasts an event whenever that state changes.
    """

    @abc.abstractmethod
    def value(self) -> T:
        """Return the current value being stored in the puddle."""
