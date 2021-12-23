from typing import Union

from garden.element import Element
from trickle import Derived, Environment, Puddle, Reposition, Surface, Visual
from trickle.visuals.overlay import Overlay


class Plant(Element):
    def __init__(
        self,
        name: Union[Puddle, str],
        size: Union[Puddle, float],
        horizontal: Union[Puddle, float] = 0.0,
        vertical: Union[Puddle, float] = 0.0,
    ):
        super().__init__(name=name, size=size, horizontal=horizontal, vertical=vertical)

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

    def plan(self, environment: Environment) -> Puddle:
        def plan(outer: float, x: float, y: float) -> Visual:
            inner = max(0, outer - 0.01)  # 1 cm border
            return Reposition(
                Overlay(
                    Reposition(
                        Surface.circle(radius=outer * 200),
                        horizontal_offset=-outer * 200,
                        vertical_offset=-outer * 200,
                    ),
                    Reposition(
                        Surface.circle(
                            radius=inner * 200, red=0.7, blue=0.4, green=0.1
                        ),
                        horizontal_offset=-inner * 200,
                        vertical_offset=-inner * 200,
                    ),
                ),
                horizontal_offset=x * 200,
                vertical_offset=y * 200,
            )

        return Derived(plan, self.size, self.horizontal, self.vertical)
