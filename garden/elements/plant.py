from typing import Union

from components.card import Card
from components.column import TextColumn
from components.component import Component
from garden.element import Element
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle import (
    Constant,
    Derived,
    Environment,
    Indexed,
    Overlay,
    Puddle,
    Reposition,
    Surface,
    Visual,
)


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

    @property
    def plan(self) -> Component:
        return Plant.Plan(self)

    @property
    def editor(self) -> Component:
        return Plant.Editor(self)

    class Plan(Component):
        def __init__(self, plant: "Plant"):
            self._plant = plant

        @staticmethod
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

        def __call__(self, environment: Environment) -> Puddle[Visual]:
            return Derived(
                self.plan,
                self._plant.size,
                self._plant.horizontal,
                self._plant.vertical,
                self._plant.red,
                self._plant.green,
                self._plant.blue,
            )

    class Editor(Component):
        def __init__(self, plant: "Plant"):
            self._plant = plant

        def __call__(self, environment: Environment) -> Puddle[Visual]:
            puddles = Indexed(
                Constant("Plant"),
                "Name: " + self._plant.name,
                "Size: " + Derived(str, self._plant.size),
                "Position: ("
                + Derived(str, self._plant.horizontal)
                + ", "
                + Derived(str, self._plant.vertical)
                + ")",
            )
            return Card(
                TextColumn(puddles, Constant(16), padding=Constant(5)),
                (0.5, 0.5, 0.5),
                5,
            )(environment)
