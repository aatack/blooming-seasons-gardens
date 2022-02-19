from typing import Callable, Optional, Union

from settings import EDITOR_TEXT_PADDING, EDITOR_TEXT_SIZE
from trickle import Environment
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived, Variable
from trickle.visuals.overlay import Overlay
from trickle.visuals.rectangle import Rectangle
from trickle.visuals.surface import Surface

from components.component import Component

BACKGROUND_COLOUR = (84 / 255, 122 / 255, 184 / 255)
HOVER_COLOUR = (121 / 255, 155 / 255, 209 / 255)
CLICK_COLOUR = (165 / 255, 190 / 255, 230 / 255)


class Button(Component):
    def __init__(self, component: Union[Component, str], callback: Callable):
        super().__init__()

        self._component = component
        self._callback = callback

        self._width_internal: Optional[Puddle] = None
        self._height_internal: Optional[Puddle] = None

    def construct(self, environment: Environment):
        if isinstance(self._component, str):
            visual = Constant(
                Surface.text(
                    self._component, EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING
                )
            )
        else:
            visual = self._component(environment)

        self._width_internal = Derived(
            lambda v, w: v.right() if w is None else w, visual, environment.screen.width
        )
        self._height_internal = Derived(
            lambda v, h: v.bottom() if h is None else h,
            visual,
            environment.screen.height,
        )

        contains_mouse = Derived(
            lambda m, w, h: 0 <= m["x"] < w and 0 <= m["y"] < h,
            environment.mouse,
            self._width_internal,
            self._height_internal,
        )
        clicked = Variable(False)

        def mouse_down():
            if contains_mouse.value():
                clicked.change(True)

        def mouse_up():
            if clicked.value():
                clicked.change(False)
                if contains_mouse.value():
                    self._callback()

        environment.mouse.add_listener(1, True, mouse_down)
        environment.mouse.add_listener(1, False, mouse_up)

        colour = Derived(
            lambda _clicked, _contains_mouse: CLICK_COLOUR
            if _clicked
            else (HOVER_COLOUR if _contains_mouse else BACKGROUND_COLOUR),
            clicked,
            contains_mouse,
        )

        self._visual = Derived(
            lambda v, w, h, c: Overlay(
                Rectangle(width=w, height=h, red=c[0], green=c[1], blue=c[2]), v
            ),
            visual,
            self._width_internal,
            self._height_internal,
            colour,
        )

    def deconstruct(self):
        pass

    def _width(self) -> Puddle[float]:
        assert self._width_internal is not None
        return self._width_internal

    def _height(self) -> Puddle[float]:
        assert self._height_internal is not None
        return self._height_internal


class Entry(Component):
    pass
