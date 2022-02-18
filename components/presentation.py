from typing import Optional, Tuple, Union

from trickle import Derived, Environment, Overlay, Puddle, puddle
from trickle.visuals.crop import Crop
from trickle.visuals.rectangle import Rectangle

from components.component import Component
from components.positioning import Move


class Fill(Component):
    def __init__(self, component: Component):
        """
        Instruct the component to fill the size of the screen given exactly.

        This will crop the component to the size of the screen, but will not make any
        visual changes if the component's visual is smaller than the screen already in a
        particular dimension.  No changes will take place if the size of the screen is
        not defined along a dimension.
        """
        super().__init__()

        self._component = component

        self._width: Optional[Puddle[float]] = None
        self._height: Optional[Puddle[float]] = None

    def construct(self, environment: Environment):
        self._width = environment.screen.width
        self._height = environment.screen.height

        self._visual = Derived(
            lambda v, w, h: Crop(
                v,
                width=w if w is not None else v.right(),
                height=h if h is not None else v.bottom(),
            ),
            self._component(environment),
            environment.screen.width,
            environment.screen.height,
        )

    def deconstruct(self):
        pass

    @property
    def bottom(self) -> Puddle[float]:
        assert self._height is not None
        return Derived(
            lambda t, h, b: t + h if h is not None else b,
            self.top,
            self._height,
            self._component.bottom,
        )

    @property
    def right(self) -> Puddle[float]:
        assert self._width is not None
        return Derived(
            lambda l, w, r: l + w if w is not None else r,
            self.left,
            self._width,
            self._component.right,
        )


class Pad(Component):
    def __init__(self, component: Component, padding: Union[Puddle, float]):
        super().__init__()

        self._component = component
        self._padding = puddle(padding)

    def construct(self, environment: Environment):
        shrunk_environment = environment.where(
            screen=environment.screen.shrink(self._padding * 2)
        )

        self._visual = Move(
            self._component, vertical=self._padding, horizontal=self._padding
        )(shrunk_environment)

    def deconstruct(self):
        pass

    def top(self) -> Puddle[float]:
        return Derived(lambda t, p: t - p, self._component.top, self._padding)

    def left(self) -> Puddle[float]:
        return Derived(lambda l, p: l - p, self._component.left, self._padding)

    def bottom(self) -> Puddle[float]:
        return Derived(lambda b, p: b + p, self._component.bottom, self._padding)

    def right(self) -> Puddle[float]:
        return Derived(lambda r, p: r + p, self._component.right, self._padding)


class Background(Component):
    def __init__(self, component: Component, colour: Tuple[float, float, float]):
        super().__init__()

        self._component = component
        self._colour = colour

    def construct(self, environment: Environment):
        visual = self._component(environment)
        self._visual = Derived(
            lambda v, r, b: Overlay(
                Rectangle(
                    width=r,
                    height=b,
                    red=self._colour[0],
                    green=self._colour[1],
                    blue=self._colour[2],
                ),
                v,
            ),
            visual,
            self._component.right,
            self._component.bottom,
        )

    def deconstruct(self):
        pass


class Card(Component):
    def __init__(
        self, component: Component, colour: Tuple[float, float, float], padding: int
    ):
        super().__init__()

        self._component = component
        self._colour = colour
        self._padding = padding

    def construct(self, environment: Environment):
        self._visual = Pad(
            Background(Fill(self._component), self._colour), self._padding
        )(environment)

    def deconstruct(self):
        pass
