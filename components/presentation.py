from typing import Tuple, Union

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


class Pad(Component):
    def __init__(self, component: Component, padding: Union[Puddle, float]):
        self._component = component
        self._padding = puddle(padding)

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        # TODO: pad the right and bottom
        return Derived(
            lambda v, p: Reposition(
                v,
                crop_right=v.horizontal_extent() + p,
                crop_bottom=v.vertical_extent() + p,
            ),
            Move(self._component, vertical=self._padding, horizontal=self._padding)(
                environment
            ),
            self._padding,
        )


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
        return Pad(Background(self._component, self._colour), self._padding)(
            environment
        )
