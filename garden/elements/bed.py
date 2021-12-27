from typing import List, Union

from components.column import Column
from components.component import Anonymous, Component
from garden.element import Element
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
            self._bed = bed

        def __call__(self, environment: Environment) -> Puddle[Visual]:
            offset_environment = environment.offset_mouse(
                Derived(lambda h: h * SCALE, self._bed.horizontal),
                Derived(lambda v: v * SCALE, self._bed.vertical),
                Constant(SCALE),
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
                    horizontal_offset=horizontal * SCALE,
                    vertical_offset=vertical * SCALE,
                )

            return Derived(plan, mapped, self._bed.horizontal, self._bed.vertical)

    class Editor(Component):
        def __init__(self, bed: "Bed"):
            self._bed = bed

        @staticmethod
        def get_inner_component(_element: Puddle) -> Component:
            """Take one of the bed's elements and reposition it."""
            return Anonymous(
                lambda _environment: Derived(
                    lambda e: Reposition(e, horizontal_offset=30),
                    _element.editor(
                        _environment.offset_mouse(
                            horizontal=Constant(30.0),
                            vertical=Constant(0.0),
                            scale=Constant(1.0),
                        )
                    ),
                )
            )

        def get_outer_component(self, _element: Puddle) -> Component:
            if _element is self._bed.elements:
                return lambda _environment: Column(_element, self.get_inner_component)(
                    _environment
                )
            else:
                return Anonymous(
                    lambda _: Derived(
                        lambda v: Surface.text(str(v), 16, padding=5), _element
                    )
                )

        def __call__(self, environment: Environment) -> Puddle[Visual]:
            puddles = Indexed(
                Constant("Bed"),
                "Position: ("
                + Derived(str, self._bed.horizontal)
                + ", "
                + Derived(str, self._bed.vertical)
                + ")",
                self._bed.elements,
            )

            return Column(puddles, self.get_outer_component)(environment)
