from typing import List, Union

from components.column import Column, ComponentColumn
from components.component import Anonymous, Component
from components.control import Button
from components.positioning import Move
from components.presentation import Background, Fill, Pad
from garden.element import Element
from settings import (
    EDITOR_BACKGROUND_COLOUR,
    EDITOR_BED_INDENT,
    EDITOR_TEXT_PADDING,
    EDITOR_TEXT_SIZE,
)
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
    Surface,
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
            elements=Indexed(*elements), horizontal=horizontal, vertical=vertical,
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
                    Overlay(*visuals), x=horizontal * SCALE, y=vertical * SCALE,
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

            expanded_puddles = Indexed(
                Constant("Bed"),
                "Position: ("
                + Derived(str, self._bed.horizontal)
                + ", "
                + Derived(str, self._bed.vertical)
                + ")",
                self._bed.elements,
            )

            # TODO: allow beds to be collapsed
            collapsed_puddles = Indexed(Constant("Bed"))

            super().__init__(
                Pad(Button("Add plant", lambda: print("Add plant")), 2),
                # STARTHERE: work out which component's bounds calculations are
                # outputting incorrect values, then fix components to simply have
                # width and height (and possibly, make them explicitly defined);
                # top and left should always be zero
                Pad(Button("Add bed", lambda: print("Add bed")), 20),
                Pad(Button("Add label", lambda: print("Add label")), 2),
                Pad(Button("Add arrow", lambda: print("Add arrow")), 2),
                Column(expanded_puddles, self.get_outer_component),
            )

        @staticmethod
        def get_inner_component(_element: Puddle) -> Component:
            """Take one of the bed's elements and reposition it."""
            return Anonymous(
                lambda e: Move(_element.editor, horizontal=EDITOR_BED_INDENT)(
                    e.where(
                        screen=e.screen.resize(
                            width=e.screen.width - EDITOR_BED_INDENT, height=None
                        )
                    )
                )
            )

        def get_outer_component(self, _element: Puddle) -> Component:
            if _element is self._bed.elements:
                return Anonymous(
                    lambda _environment: Column(_element, self.get_inner_component)(
                        _environment
                    )
                )
            else:
                return Anonymous(
                    lambda _: Derived(
                        lambda v: Surface.text(
                            str(v), EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING
                        ),
                        _element,
                    )
                )
