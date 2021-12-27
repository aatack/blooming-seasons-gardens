from typing import Tuple

from trickle.environment import Environment
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Derived
from trickle.visuals.overlay import Overlay
from trickle.visuals.reposition import Reposition
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual

from components.component import Component


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
