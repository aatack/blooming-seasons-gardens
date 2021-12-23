import abc
from typing import Any, Union

from trickle import Keyed, puddle
from trickle.trickles.puddle import Puddle


class Element(Keyed, abc.ABC):
    """Base class for elements of a garden."""

    def __init__(self, **attributes: Union[Puddle, Any]):
        Keyed.__init__(
            self,
            **{attribute: puddle(value) for attribute, value in attributes.items()}
        )
