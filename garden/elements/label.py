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
from trickle import Derived, Puddle, Reposition, Surface, Visual


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

    class Plan(Anonymous):
        def __init__(self, label: "Label"):
            self._label = label

            super().__init__(
                lambda _: Derived(
                    self.plan,
                    self._label.text,
                    self._label.size,
                    self._label.horizontal,
                    self._label.vertical,
                )
            )

        @staticmethod
        def plan(text: str, size: int, x: float, y: float) -> Visual:
            return Reposition(Surface.text(text, size), x=x * SCALE, y=y * SCALE,)

    class Editor(Card):
        def __init__(self, label: "Label"):
            self._label = label

            def text(string: Union[Puddle, str]) -> Component:
                return Text(string, EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING)

            super().__init__(
                ComponentColumn(
                    text("Label"),
                    ComponentRow(
                        text("Text: "), Entry(self._label.text, Entry.Converters.string)
                    ),
                    ComponentRow(
                        text("Size: "),
                        Entry(self._label.size, Entry.Converters.integer),
                    ),
                    ComponentRow(
                        text("Position: ("),
                        Entry(self._label.horizontal, Entry.Converters.float),
                        text(", "),
                        Entry(self._label.vertical, Entry.Converters.float),
                        text(")"),
                    ),
                ),
                EDITOR_BLOCK_COLOUR,
                EDITOR_PADDING,
            )
