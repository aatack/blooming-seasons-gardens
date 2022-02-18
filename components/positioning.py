from typing import Union

from trickle import Derived, Environment, Puddle, Reposition, Visual, puddle
from trickle.trickles.singular import Variable

from components.component import Component


class Move(Component):
    def __init__(
        self,
        component: Component,
        horizontal: Union[Puddle, float] = 0.0,
        vertical: Union[Puddle, float] = 0.0,
    ):
        super().__init__()

        self._component = component
        self._horizontal = puddle(horizontal)
        self._vertical = puddle(vertical)

    def construct(self, environment: Environment):
        self._visual = Derived(
            lambda v, x, y: Reposition(v, x=x, y=y),
            self._component(
                environment.where(
                    mouse=environment.mouse.offset(
                        horizontal=self._horizontal, vertical=self._vertical
                    )
                )
            ),
            self._horizontal,
            self._vertical,
        )

    def deconstruct(self):
        pass


class Scroll(Component):
    SCROLL_DOWN_BUTTON = 5
    SCROLL_UP_BUTTON = 4

    def __init__(self, component: Component, scroll_speed: float = 25.0):
        super().__init__()

        self._component = component
        self._scroll_speed = scroll_speed
        self._scroll_position = Variable(0)

        # Amount by which the environment height is less than the component height; used
        # to clip the scroll position appropriately
        self._height_deficit: Puddle[float] = Variable(0.0)

    def scroll_down(self, active: Puddle[bool]):
        def scroll_down():
            if active.value():
                deficit = self._height_deficit.value()
                self._scroll_position.change_as_function(
                    lambda s: max(
                        -deficit if deficit >= 0 else 0, s - self._scroll_speed
                    )
                )

        return scroll_down

    def scroll_up(self, active: Puddle[bool]):
        def scroll_up():
            if active.value():
                self._scroll_position.change_as_function(
                    lambda s: min(0, s + self._scroll_speed)
                )

        return scroll_up

    def construct(self, environment: Environment):
        environment.mouse.add_listener(
            self.SCROLL_DOWN_BUTTON,
            True,
            self.scroll_down(environment.screen.contains_mouse(environment.mouse)),
        )
        environment.mouse.add_listener(
            self.SCROLL_UP_BUTTON,
            True,
            self.scroll_up(environment.screen.contains_mouse(environment.mouse)),
        )

        component = self._component(
            environment.where(
                mouse=environment.mouse.offset(vertical=self._scroll_position)
            )
        )

        self._height_deficit = Derived(
            lambda c, h: c.bottom() - h, component, environment.screen.height
        )

        self._visual = Derived(
            lambda c, y: Reposition(c, y=y), component, self._scroll_position,
        )

    def deconstruct(self):
        pass