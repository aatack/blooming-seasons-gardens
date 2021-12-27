import abc
from typing import Any, Union

from components.component import Component
from trickle import Keyed, Puddle, puddle


class Element(Keyed, abc.ABC):
    """Base class for elements of a garden."""

    def __init__(self, **attributes: Union[Puddle, Any]):
        Keyed.__init__(
            self,
            **{attribute: puddle(value) for attribute, value in attributes.items()}
        )

    @abc.abstractproperty
    def plan(self) -> Component:
        """
        Return a component defining a visual representation of the garden element.

        The visual representation should be from a top-down (plan) view, as the plant
        will appear in the final plan.  It may also respond to user inputs.
        """
        # TODO: we will need a way to ensure that any side effects (ie. any way in which
        #       this function makes the underlying element respond to events from the
        #       mouse environment) are cleared when `isolate()` is called on the
        #       resulting puddle

    @abc.abstractproperty
    def editor(self) -> Component:
        """Return a component defining an editor for the garden element."""
        # TODO: we will need a way to ensure that any side effects (ie. any way in which
        #       this function makes the underlying element respond to events from the
        #       mouse environment) are cleared when `isolate()` is called on the
        #       resulting puddle
