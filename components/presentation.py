from typing import Optional, Tuple, Union

from trickle import (
    Derived,
    Environment,
    Overlay,
    Puddle,
    Reposition,
    Surface,
    Visual,
    puddle,
)
from trickle.visuals.crop import Crop

from components.component import Component
from components.positioning import Move


class Fill(Component):
    def __init__(self, component: Component):
        """
        Instruct the component to fill the size of the screen given exactly.

        This will crop the component to the size of the screen, but will not make any
        visual changes if the component's visual is smaller than the screen already in a
        particular dimension.  No changes will take place if the size of the screen is
        not defined along a dimension.

        Note that this is similar to applying a pad operation with a zero pad size.
        """
        super().__init__()

        self._component = component

    def construct(self, environment: Environment):
        self._visual = Derived(
            lambda v, w, h: Crop(
                v,
                width=w if w is not None else v.right(),
                height=h if h is not None else v.bottom(),
            ),
            self._component(environment),
            environment.screen.width,
            environment.screen.height,
        )

    def deconstruct(self):
        pass


class Pad(Component):
    def __init__(self, component: Component, padding: Union[Puddle, float]):
        super().__init__()

        self._component = component
        self._padding = puddle(padding)

    def construct(self, environment: Environment):
        shrunk_environment = environment.where(
            screen=environment.screen.shrink(self._padding * 2)
        )

        self._visual = Derived(
            lambda v, p, w, h: Reposition(
                v,
                # TODO: work out why uncommenting the below causes buggy behaviour
                # crop_right=self.crop_size(v.horizontal_extent(), p, w),
                # crop_bottom=self.crop_size(v.vertical_extent(), p, h),
            ),
            Move(self._component, vertical=self._padding, horizontal=self._padding)(
                shrunk_environment
            ),
            self._padding,
            shrunk_environment.screen.width,
            shrunk_environment.screen.height,
        )

    def deconstruct(self):
        pass

    @staticmethod
    def crop_size(extent: float, padding: float, window: Optional[float]) -> float:
        return window + (2 * padding) if window is not None else extent + padding


class Background(Component):
    def __init__(self, component: Component, colour: Tuple[float, float, float]):
        super().__init__()

        self._component = component
        self._colour = colour

    def construct(self, environment: Environment):
        visual = self._component(environment)
        self._visual = Derived(
            lambda v, r, b: Overlay(
                Surface.rectangle(
                    r,
                    b,
                    red=self._colour[0],
                    green=self._colour[1],
                    blue=self._colour[2],
                ),
                v,
            ),
            visual,
            self._component.right,
            self._component.bottom,
        )

    def deconstruct(self):
        pass


class Card(Component):
    def __init__(
        self, component: Component, colour: Tuple[float, float, float], padding: int
    ):
        super().__init__()

        self._component = component
        self._colour = colour
        self._padding = padding

    def construct(self, environment: Environment):
        self._visual = Pad(
            Background(Fill(self._component), self._colour), self._padding
        )(environment)

    def deconstruct(self):
        pass
