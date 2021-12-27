import abc
from typing import Any, Callable, Generic, TypeVar

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
        return _derived(lambda left, right: left + right, self, other)

    def __radd__(self, other: Any) -> "Puddle":
        return type(self).__add__(other, self)

    def __mul__(self, other: Any) -> "Puddle":
        return _derived(lambda left, right: left * right, self, other)

    def __rmul__(self, other: Any) -> "Puddle":
        return type(self).__mul__(other, self)

    def __sub__(self, other: Any) -> "Puddle":
        return _derived(lambda left, right: left - right, self, other)

    def __rsub__(self, other: Any) -> "Puddle":
        return type(self).__sub__(other, self)

    def __truediv__(self, other: Any) -> "Puddle":
        return _derived(lambda left, right: left / right, self, other)

    def __rtruediv__(self, other: Any) -> "Puddle":
        return type(self).__truediv__(other, self)

    def log(self, message: str) -> "Puddle":
        from trickle.trickles.log import Log

        log = Log(message)
        log.listen((message,), self)
        return self


def _derived(function: Callable, left: Any, right: Any) -> Puddle:
    from trickle.trickles.singular import Constant, Derived

    return Derived(
        function,
        left if isinstance(left, Puddle) else Constant(left),
        right if isinstance(right, Puddle) else Constant(right),
    )


def puddle(value: Any) -> Puddle:
    if isinstance(value, Puddle):
        return value
    else:
        from trickle.trickles.singular import Variable

        return Variable(value)
