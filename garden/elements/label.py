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
            super().__init__()

            self._label = label

        @staticmethod
        def plan(text: str, size: int, x: float, y: float) -> Visual:
            return Reposition(Surface.text(text, size), x=x * SCALE, y=y * SCALE,)

        def construct(self, environment: Environment):
            self._visual = Derived(
                self.plan,
                self._label.text,
                self._label.size,
                self._label.horizontal,
                self._label.vertical,
            )

            # TODO: check this environment is correct
            self._environment = environment

        def deconstruct(self):
            pass

    class Editor(Component):
        def __init__(self, label: "Label"):
            super().__init__()

            self._label = label

        def construct(self, environment: Environment):
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
