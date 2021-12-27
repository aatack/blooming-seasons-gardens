from typing import Union

import pygame
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
        self._component = component
        self._horizontal = puddle(horizontal)
        self._vertical = puddle(vertical)

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        return Derived(
            lambda v, x, y: Reposition(v, horizontal_offset=x, vertical_offset=y),
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


class Scroll(Component):
    SCROLL_DOWN_BUTTON = 5
    SCROLL_UP_BUTTON = 4

    def __init__(self, component: Component, scroll_speed: float = 25.0):
        self._component = component
        self._scroll_speed = scroll_speed
        self._scroll_position = Variable(0)

    def scroll_down(self, active: Puddle[bool]):
        def scroll_down():
            if active.value():
                self._scroll_position.change_as_function(
                    lambda s: s - self._scroll_speed
                )

        return scroll_down

    def scroll_up(self, active: Puddle[bool]):
        def scroll_up():
            if active.value():
                self._scroll_position.change_as_function(
                    lambda s: s + self._scroll_speed
                )

        return scroll_up

    def __call__(self, environment: Environment) -> Puddle[Visual]:
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

        return Move(self._component, vertical=self._scroll_position)(environment)
