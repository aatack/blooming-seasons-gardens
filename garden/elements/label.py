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
    Puddle,
    Reposition,
    Surface,
    Visual,
)


class Label(Element):
    def __init__(
        self,
        text: Union[str, Puddle],
        size: Union[int, Puddle] = 24,
        horizontal: Union[float, Puddle] = 0.0,
        vertical: Union[float, Puddle] = 0.0,
    ):
        super().__init__(text=text, size=size, horizontal=horizontal, vertical=vertical)

    @property
    def text(self) -> Puddle:
        return self["text"]

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
    def plan(self) -> Component:
        return Label.Plan(self)

    @property
    def editor(self) -> Component:
        return Label.Editor(self)

    class Plan(Component):
        def __init__(self, label: "Label"):
            self._label = label

        @staticmethod
        def plan(text: str, size: int, x: float, y: float) -> Visual:
            return Reposition(
                Surface.text(text, size),
                horizontal_offset=x * SCALE,
                vertical_offset=y * SCALE,
            )

        def __call__(self, environment: Environment) -> Puddle[Visual]:
            return Derived(
                self.plan,
                self._label.text,
                self._label.size,
                self._label.horizontal,
                self._label.vertical,
            )

    class Editor(Component):
        def __init__(self, label: "Label"):
            self._label = label

        def __call__(self, environment: Environment) -> Puddle[Visual]:
            puddles = Indexed(
                Constant("Label"),
                "Text: " + Derived(str, self._label.text),
                "Size: " + Derived(str, self._label.size),
                "Position: ("
                + Derived(str, self._label.horizontal)
                + ", "
                + Derived(str, self._label.vertical)
                + ")",
            )

            return Card(
                TextColumn(puddles, Constant(16), padding=Constant(5)),
                (0.5, 0.5, 0.5),
                5,
            )(environment)
