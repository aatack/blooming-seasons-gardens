from typing import Union

from components.column import TextColumn
from components.component import Component
from components.presentation import Card
from garden.element import Element
from settings import (
    EDITOR_BLOCK_COLOUR,
    EDITOR_PADDING,
    EDITOR_TEXT_PADDING,
    EDITOR_TEXT_SIZE,
)
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
            super().__init__()

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
                        x=-outer * SCALE,
                        y=-outer * SCALE,
                    ),
                    Reposition(
                        Surface.circle(
                            radius=inner * SCALE, red=red, green=green, blue=blue
                        ),
                        x=-inner * SCALE,
                        y=-inner * SCALE,
                    ),
                ),
                x=x * SCALE,
                y=y * SCALE,
            )

        def construct(self, environment: Environment):
            self._visual = Derived(
                self.plan,
                self._plant.size,
                self._plant.horizontal,
                self._plant.vertical,
                self._plant.red,
                self._plant.green,
                self._plant.blue,
            )

            # TODO: check this environment is correct
            self._environment = environment

        def deconstruct(self):
            pass

    class Editor(Component):
        def __init__(self, plant: "Plant"):
            super().__init__()

            self._plant = plant

        def construct(self, environment: Environment):
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
            self._visual = Card(
                TextColumn(
                    puddles,
                    Constant(EDITOR_TEXT_SIZE),
                    padding=Constant(EDITOR_TEXT_PADDING),
                ),
                EDITOR_BLOCK_COLOUR,
                EDITOR_PADDING,
            )(environment)

            # TODO: check this environment is correct
            self._environment = environment

        def deconstruct(self):
            pass
