from typing import Callable, Union

from settings import EDITOR_TEXT_PADDING, EDITOR_TEXT_SIZE
from trickle import Environment
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived, Variable
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual

from components.component import Component


class Button(Component):
    def __init__(self, component: Union[Component, str], callback: Callable):
        super().__init__()

        self._component = component
        self._callback = callback

    def __call__(self, environment: Environment) -> Puddle[Visual]:
        if isinstance(self._component, str):
            visual = Constant(
                Surface.text(
                    self._component, EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING
                )
            )
        else:
            visual = self._component(environment)

        contains_mouse = Derived(
            lambda m, w, h: 0 <= m["x"] < w and 0 <= m["y"] < h,
            environment.mouse,
            Derived(lambda v: v.horizontal_extent(), visual),
            Derived(lambda v: v.vertical_extent(), visual),
        )
        clicked = Variable(False)

        def mouse_down():
            if contains_mouse.value():
                clicked.change(True)

        def mouse_up():
            if clicked.value() and contains_mouse.value():
                self._callback()
            clicked.change(False)

        environment.mouse.add_listener(1, True, mouse_down)
        environment.mouse.add_listener(1, False, mouse_up)

        return visual


class Entry(Component):
    pass
