import abc
from typing import Any, Union

from trickle import Keyed, puddle
from trickle.environment import Environment
from trickle.trickles.puddle import Puddle


class Element(Keyed, abc.ABC):
    """Base class for elements of a garden."""

    def __init__(self, **attributes: Union[Puddle, Any]):
        Keyed.__init__(
            self,
            **{attribute: puddle(value) for attribute, value in attributes.items()}
        )

    @abc.abstractmethod
    def plan(self, environment: Environment) -> Puddle:
        """
        Return a puddle containing a visual representation of the garden element.
        
        The visual representation should be from a top-down (plan) view, as the plant
        will appear in the final plan.  It may also respond to user inputs.
        """
