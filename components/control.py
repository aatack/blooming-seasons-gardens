from typing import Any, Callable, Optional, Union

from settings import EDITOR_TEXT_PADDING, EDITOR_TEXT_SIZE
from trickle import Environment
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived, Variable
from trickle.visuals.empty import Empty
from trickle.visuals.overlay import Overlay
from trickle.visuals.rectangle import Rectangle
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual

from components.component import Component, Wrap

BACKGROUND_COLOUR = (84 / 255, 122 / 255, 184 / 255)
HOVER_COLOUR = (121 / 255, 155 / 255, 209 / 255)
CLICK_COLOUR = (165 / 255, 190 / 255, 230 / 255)


class ChangeEnvironment(Wrap):
    def __init__(
        self, function: Callable[[Environment], Environment], component: Component
    ):
        super().__init__(component)

        self._function = function

    def construct(self, environment: Environment):
        self._visual = self._component(self._function(environment))


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

    SELECTED_COLOUR = {"red": 152 / 255, "green": 203 / 255, "blue": 250 / 255}
    UNSELECTED_COLOUR = {"red": 1.0, "green": 1.0, "blue": 1.0}

    def __init__(self, variable: Variable):
        super().__init__()

        self._variable = variable

        self._selected = Variable(False)
        self._selected.log(lambda v: v.value())

    def construct(self, environment: Environment):
        self._visual = Derived(self._build_visual, self._variable, self._selected)

        contains_mouse = Derived(
            lambda m, w, h: 0 <= m["x"] < w and 0 <= m["y"] < h,
            environment.mouse,
            self.width,
            self.height,
        )
        clicked = Variable(False)

        def mouse_down():
            if contains_mouse.value():
                clicked.change(True)
            else:
                self._selected.change(False)

        def mouse_up():
            if clicked.value():
                clicked.change(False)
                if contains_mouse.value():
                    self._selected.change(True)

        environment.mouse.add_listener(1, True, mouse_down)
        environment.mouse.add_listener(1, False, mouse_up)

    @classmethod
    def _build_visual(cls, value: Any, selected: bool) -> Visual:
        text = Surface.text(str(value), EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING)
        background = Rectangle(
            width=text.right(),
            height=text.bottom(),
            **(cls.SELECTED_COLOUR if selected else cls.UNSELECTED_COLOUR)
        )

        return Overlay(background, text)

    def deconstruct(self):
        pass

    def _width(self) -> Puddle[float]:
        return Derived(lambda v: v.right(), self._visual)

    def _height(self) -> Puddle[float]:
        return Derived(lambda v: v.bottom(), self._visual)
