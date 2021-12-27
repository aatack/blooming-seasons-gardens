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
        self._component = component

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        return Derived(
            lambda v, w, h: Reposition(
                v,
                crop_right=w if w is not None else v.horizontal_extent(),
                crop_bottom=h if h is not None else v.vertical_extent(),
            ),
            self._component(environment),
            environment.screen.width,
            environment.screen.height,
        )


class Pad(Component):
    def __init__(self, component: Component, padding: Union[Puddle, float]):
        self._component = component
        self._padding = puddle(padding)

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        shrunk_environment = environment.shrink_screen(self._padding * 2)
        return Derived(
            lambda v, p, w, h: Reposition(
                v,
                crop_right=self.crop_size(v.horizontal_extent(), p, w),
                crop_bottom=self.crop_size(v.vertical_extent(), p, h),
            ),
            Move(self._component, vertical=self._padding, horizontal=self._padding)(
                shrunk_environment
            ),
            self._padding,
            shrunk_environment.screen.width,
            shrunk_environment.screen.height,
        )

    @staticmethod
    def crop_size(extent: float, padding: float, window: Optional[float]) -> float:
        return window + (2 * padding) if window is not None else extent + padding


class Background(Component):
    def __init__(self, component: Component, colour: Tuple[float, float, float]):
        self._component = component
        self._colour = colour

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        visual = self._component(environment)
        return Derived(
            lambda v: Overlay(
                Surface.rectangle(
                    v.horizontal_extent(),
                    v.vertical_extent(),
                    red=self._colour[0],
                    green=self._colour[1],
                    blue=self._colour[2],
                ),
                v,
            ),
            visual,
        )


class Card(Component):
    def __init__(
        self, component: Component, colour: Tuple[float, float, float], padding: int
    ):
        self._component = component
        self._colour = colour
        self._padding = padding

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        return Pad(Background(Fill(self._component), self._colour), self._padding)(
            environment
        )
