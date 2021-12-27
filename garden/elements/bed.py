from typing import List, Union

from garden.element import Element
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle import Indexed
from trickle.components.column import column
from trickle.environment import Environment
from trickle.trickles.indexed import Mapped
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived
from trickle.visuals.overlay import Overlay
from trickle.visuals.reposition import Reposition
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


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

    def plan(self, environment: Environment) -> Puddle:
        offset_environment = environment.offset_mouse(
            Derived(lambda h: h * SCALE, self.horizontal),
            Derived(lambda v: v * SCALE, self.vertical),
            Constant(SCALE),
        )

        mapped = Mapped(
            lambda e: e.plan(offset_environment), self.elements, function_of_puddle=True
        )

        def plan(visuals: List[Visual], horizontal: float, vertical: float) -> Visual:
            return Reposition(
                Overlay(*visuals),
                horizontal_offset=horizontal * SCALE,
                vertical_offset=vertical * SCALE,
            )

        return Derived(plan, mapped, self.horizontal, self.vertical)

    def editor(self, environment: Environment) -> Puddle:
        def build_inner_visual(
            _element: Puddle, _environment: Environment
        ) -> Puddle[Visual]:
            return Derived(
                lambda e: Reposition(e, horizontal_offset=30),
                _element.editor(
                    _environment.offset_mouse(
                        horizontal=Constant(30.0),
                        vertical=Constant(0.0),
                        scale=Constant(1.0),
                    )
                ),
            )

        def build_outer_visual(
            _element: Puddle, _environment: Environment
        ) -> Puddle[Visual]:
            if _element is self.elements:
                return column(_environment, _element, build_inner_visual)
            else:
                return Derived(lambda v: Surface.text(str(v), 16, padding=5), _element)

        elements = Indexed(
            Constant("Bed"),
            "Position: ("
            + Derived(str, self.horizontal)
            + ", "
            + Derived(str, self.vertical)
            + ")",
            self.elements,
        )

        return column(environment, elements, build_outer_visual)
