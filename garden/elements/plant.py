from typing import Union

from components.column import ComponentColumn
from components.component import Anonymous, Component
from components.control import Entry
from components.presentation import Card
from components.row import ComponentRow
from components.text import Text
from garden.element import Element
from settings import (
    EDITOR_BLOCK_COLOUR,
    EDITOR_PADDING,
    EDITOR_TEXT_PADDING,
    EDITOR_TEXT_SIZE,
)
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle import Derived, Overlay, Puddle, Reposition, Surface, Visual


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

    class Plan(Anonymous):
        def __init__(self, plant: "Plant"):
            self._plant = plant

            super().__init__(
                lambda _: Derived(
                    self.plan,
                    self._plant.size,
                    self._plant.horizontal,
                    self._plant.vertical,
                    self._plant.red,
                    self._plant.green,
                    self._plant.blue,
                )
            )

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

    class Editor(Card):
        def __init__(self, plant: "Plant"):
            self._plant = plant

            def text(string: Union[Puddle, str]) -> Component:
                return Text(string, EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING)

            super().__init__(
                ComponentColumn(
                    text("Plant"),
                    text("Name: " + self._plant.name),
                    text(
                        "Position: ("
                        + Derived(str, self._plant.horizontal)
                        + ", "
                        + Derived(str, self._plant.vertical)
                        + ")"
                    ),
                    ComponentRow(
                        text("Size:"), Entry(self._plant.size, Entry.Converters.float)
                    ),
                ),
                EDITOR_BLOCK_COLOUR,
                EDITOR_PADDING,
            )
