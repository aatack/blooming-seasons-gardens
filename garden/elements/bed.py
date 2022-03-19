from typing import List, Union

from components.column import Column, ComponentColumn
from components.component import Component
from components.control import Button, ChangeEnvironment
from components.positioning import Move
from components.presentation import Pad
from components.row import ComponentRow
from components.text import Text
from garden.element import Element
from garden.elements.arrow import Arrow
from garden.elements.label import Label
from garden.elements.plant import Plant
from settings import EDITOR_BED_INDENT, EDITOR_TEXT_PADDING, EDITOR_TEXT_SIZE
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle import (
    Constant,
    Derived,
    Environment,
    Indexed,
    Mapped,
    Overlay,
    Puddle,
    Reposition,
    Visual,
)
from trickle.trickles.singular import Variable


class Bed(Element):
    def __init__(
        self,
        elements: List[Element],
        horizontal: Union[float, Puddle] = 0.0,
        vertical: Union[float, Puddle] = 0.0,
    ):
        assert isinstance(elements, List)
        for element in elements:
            assert isinstance(element, Element)

        super().__init__(
            elements=Indexed(*elements),
            horizontal=horizontal,
            vertical=vertical,
        )

    @property
    def elements(self) -> Indexed:
        elements = self["elements"]
        assert isinstance(elements, Indexed)
        return elements

    @property
    def horizontal(self) -> Puddle:
        return self["horizontal"]

    @property
    def vertical(self) -> Puddle:
        return self["vertical"]

    @property
    def plan(self) -> Component:
        return Bed.Plan(self)

    @property
    def editor(self) -> Component:
        return Bed.Editor(self)

    class Plan(Component):
        def __init__(self, bed: "Bed"):
            super().__init__()

            self._bed = bed

        def construct(self, environment: Environment):
            offset_environment = environment.where(
                mouse=environment.mouse.offset(
                    Derived(lambda h: h * SCALE, self._bed.horizontal),
                    Derived(lambda v: v * SCALE, self._bed.vertical),
                    Constant(SCALE),
                )
            )

            mapped = Mapped(
                lambda e: e.plan(offset_environment),
                self._bed.elements,
                function_of_puddle=True,
            )

            def plan(
                visuals: List[Visual], horizontal: float, vertical: float
            ) -> Visual:
                return Reposition(
                    Overlay(*visuals),
                    x=horizontal * SCALE,
                    y=vertical * SCALE,
                )

            self._visual = Derived(
                plan, mapped, self._bed.horizontal, self._bed.vertical
            )

        def deconstruct(self):
            pass

        def _width(self) -> Puddle[float]:
            return Derived(lambda v: v.right(), self._visual)

        def _height(self) -> Puddle[float]:
            return Derived(lambda v: v.bottom(), self._visual)

    class Editor(ComponentColumn):
        def __init__(self, bed: "Bed"):
            self._bed = bed
            self._collapsed = Variable(False)

            # TODO: allow beds to be collapsed
            _ = Indexed(Constant("Bed"))

            def text(string: Union[Puddle, str]) -> Component:
                return Text(string, EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING)

            super().__init__(
                text("Bed"),
                text(
                    "Position: ("
                    + Derived(str, self._bed.horizontal)
                    + ", "
                    + Derived(str, self._bed.vertical)
                    + ")"
                ),
                ComponentRow(
                    Pad(Button("Add plant", lambda: self.add_plant("Plant", 0.1)), 2),
                    Pad(Button("Add bed", lambda: self.add_bed([])), 2),
                    Pad(Button("Add label", lambda: self.add_label("Label")), 2),
                    Pad(
                        Button("Add arrow", lambda: self.add_arrow(0.0, 0.0, 0.5, 0.5)),
                        2,
                    ),
                ),
                Column(self._bed.elements, self._child_element),
            )

        @staticmethod
        def _child_element(element: Puddle) -> Component:
            """Take one of the bed's elements and reposition it."""
            assert isinstance(element, Element)
            return ChangeEnvironment(
                lambda e: e.where(
                    screen=e.screen.resize(
                        width=e.screen.width - EDITOR_BED_INDENT, height=None
                    )
                ),
                Move(element.editor, horizontal=EDITOR_BED_INDENT),
            )

        def add_plant(self, *args, **kwargs):
            self._bed.elements.add(Plant(*args, **kwargs))

        def add_bed(self, *args, **kwargs):
            self._bed.elements.add(Bed(*args, **kwargs))

        def add_label(self, *args, **kwargs):
            self._bed.elements.add(Label(*args, **kwargs))

        def add_arrow(self, *args, **kwargs):
            self._bed.elements.add(Arrow(*args, **kwargs))
