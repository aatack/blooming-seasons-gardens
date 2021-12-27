from typing import Optional, Union

from garden.element import Element
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle import Derived, Environment, Puddle, Reposition, Surface, Visual


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

    def plan(self, environment: Environment) -> Puddle:
        def plan(text: str, size: int, x: float, y: float) -> Visual:
            return Reposition(
                Surface.text(text, size),
                horizontal_offset=x * SCALE,
                vertical_offset=y * SCALE,
            )

        return Derived(plan, self.text, self.size, self.horizontal, self.vertical)

    def editor(self, environment: Environment) -> Puddle:
        def editor(width: Optional[float], height: Optional[float]) -> Visual:
            assert width is not None
            assert height is None
            return Surface.rectangle(width, 100, green=0.5, blue=0.5)

        return Derived(editor, environment.screen.width, environment.screen.height)
