from typing import Any, Callable, Optional, Union

import pygame
from settings import EDITOR_TEXT_PADDING, EDITOR_TEXT_SIZE
from trickle import Environment
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived, Pointer, Variable
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
    class InvalidConversion(Exception):
        pass

    class Converters:
        @staticmethod
        def float(string: str) -> float:
            try:
                return float(string)
            except ValueError:
                raise Entry.InvalidConversion

    SELECTED_COLOUR = {"red": 152 / 255, "green": 203 / 255, "blue": 250 / 255}
    UNSELECTED_COLOUR = {"red": 1.0, "green": 1.0, "blue": 1.0}
    INVALID_COLOUR = {"red": 247 / 255, "green": 104 / 255, "blue": 104 / 255}

    def __init__(self, variable: Variable, converter: Callable[[str], Any]):
        super().__init__()

        self._variable = variable
        self._converter = converter

        self._selected = Variable(False)
        self._string = Variable("")
        self._error = Variable(False)

        self._environment: Optional[Environment] = None

    def construct(self, environment: Environment):
        self._environment = environment

        variable = Pointer(
            lambda s: self._string if s.value() else self._variable, self._selected,
        )
        self._visual = Derived(
            self._build_visual, variable, self._selected, self._error
        )

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
                self._end_selected()

        def mouse_up():
            if clicked.value():
                clicked.change(False)
                if contains_mouse.value():
                    self._begin_selected()

        environment.mouse.add_listener(1, True, mouse_down)
        environment.mouse.add_listener(1, False, mouse_up)

        environment.keyboard.general_listeners.append(self._key)

    def _begin_selected(self):
        self._string.change(str(self._variable.value()))
        self._selected.change(True)

    def _end_selected(self):
        self._selected.change(False)

    def _update_underlying_variable(self, value: str):
        self._string.change(value)
        try:
            self._variable.change(self._converter(self._string.value()))
            self._error.change(False)
        except self.InvalidConversion:
            self._error.change(True)

    @classmethod
    def _build_visual(cls, value: Any, selected: bool, error: bool) -> Visual:
        text = Surface.text(str(value), EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING)
        background = Rectangle(
            width=text.right(),
            height=text.bottom(),
            **(
                (cls.INVALID_COLOUR if error else cls.SELECTED_COLOUR)
                if selected
                else cls.UNSELECTED_COLOUR
            )
        )

        return Overlay(background, text)

    def _key(self, key: int, down: bool):
        if not self._selected.value() or not down:
            return

        if key == pygame.K_SPACE:
            self._update_underlying_variable(self._string.value() + " ")
        elif key == pygame.K_BACKSPACE:
            if pygame.K_LCTRL in self._environment.keyboard.held:
                self._update_underlying_variable("")
            else:
                self._update_underlying_variable(self._string.value()[:-1])
        elif key == pygame.K_RETURN:
            self._end_selected()
        else:
            character = pygame.key.name(key)
            if len(character) == 1:
                self._update_underlying_variable(self._string.value() + character)

    def deconstruct(self):
        pass

    def _width(self) -> Puddle[float]:
        return Derived(lambda v: v.right(), self._visual)

    def _height(self) -> Puddle[float]:
        return Derived(lambda v: v.bottom(), self._visual)
