from typing import Union

from garden.element import Element
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle import Derived, Environment, Overlay, Puddle, Reposition, Surface, Visual
from trickle.components.card import card
from trickle.components.column import text_column
from trickle.trickles.indexed import Indexed
from trickle.trickles.singular import Constant


class Plant(Element):
    def __init__(
        self,
        name: Union[Puddle, str],
        size: Union[Puddle, float],
        horizontal: Union[Puddle, float] = 0.0,
        vertical: Union[Puddle, float] = 0.0,
        red: Union[Puddle, float] = 0.0,
        green: Union[Puddle, float] = 0.0,
        blue: Union[Puddle, float] = 0.0,
    ):
        super().__init__(
            name=name,
            size=size,
            horizontal=horizontal,
            vertical=vertical,
            red=red,
            green=green,
            blue=blue,
        )

    @property
    def name(self) -> Puddle:
        return self["name"]

    @property
    def size(self) -> Puddle:
        return self["size"]

    @property
    def horizontal(self) -> Puddle:
        return self["horizontal"]

    @property
    def vertical(self) -> Puddle:
        return self["vertical"]

    @property
    def red(self) -> Puddle:
        return self["red"]

    @property
    def green(self) -> Puddle:
        return self["green"]

    @property
    def blue(self) -> Puddle:
        return self["blue"]

    def plan(self, environment: Environment) -> Puddle:
        def plan(
            outer: float, x: float, y: float, red: float, green: float, blue: float
        ) -> Visual:
            inner = max(0, outer - 0.01)  # 1 cm border
            return Reposition(
                Overlay(
                    Reposition(
                        Surface.circle(radius=outer * SCALE),
                        horizontal_offset=-outer * SCALE,
                        vertical_offset=-outer * SCALE,
                    ),
                    Reposition(
                        Surface.circle(
                            radius=inner * SCALE, red=red, green=green, blue=blue
                        ),
                        horizontal_offset=-inner * SCALE,
                        vertical_offset=-inner * SCALE,
                    ),
                ),
                horizontal_offset=x * SCALE,
                vertical_offset=y * SCALE,
            )

        return Derived(
            plan,
            self.size,
            self.horizontal,
            self.vertical,
            self.red,
            self.green,
            self.blue,
        )

    def editor(self, environment: Environment) -> Puddle:
        return card(text_column, (0.5, 0.5, 0.5), 5, Constant(16), padding=Constant(5))(
            environment,
            Indexed(
                Constant("Plant"),
                "Name: " + self.name,
                "Size: " + Derived(str, self.size),
                "Position: ("
                + Derived(str, self.horizontal)
                + ", "
                + Derived(str, self.vertical)
                + ")",
            ),
        )
