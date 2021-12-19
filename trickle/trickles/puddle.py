import abc
from typing import Generic, TypeVar

from trickle.trickles.trickle import Trickle

T = TypeVar("T")


class Puddle(Trickle, Generic[T]):
    @abc.abstractmethod
    def value(self) -> T:
        """Return the current value being stored in the puddle."""
