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


class Pad(Component):
    def __init__(self, component: Component, padding: Union[Puddle, float]):
        self._component = component
        self._padding = puddle(padding)

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        raise NotImplementedError()


class Card(Component):
    def __init__(
        self, component: Component, colour: Tuple[float, float, float], border: int
    ):
        self._component = component
        self._colour = colour
        self._border = border

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        return Derived(
            lambda v: Reposition(
                Overlay(
                    Reposition(
                        Surface.rectangle(
                            v.horizontal_extent(),
                            v.vertical_extent(),
                            red=self._colour[0],
                            green=self._colour[1],
                            blue=self._colour[2],
                        ),
                        crop_left=-self._border,
                        crop_right=v.horizontal_extent() + self._border,
                        crop_top=-self._border,
                        crop_bottom=v.vertical_extent() + self._border,
                    ),
                    v,
                ),
                horizontal_offset=self._border,
                vertical_offset=self._border,
            ),
            self._component(environment),
        )
