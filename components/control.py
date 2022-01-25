from typing import Callable, Union

from settings import EDITOR_TEXT_PADDING, EDITOR_TEXT_SIZE
from trickle import environment
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual

from components.component import Component


class Button(Component):
    def __init__(self, component: Union[Component, str], callback: Callable):
        super().__init__()

        self._component = component
        self._callback = callback

    def __call__(self, environment: environment) -> Puddle[Visual]:
        if isinstance(self._component, str):
            return Constant(
                Surface.text(
                    self._component, EDITOR_TEXT_SIZE, padding=EDITOR_TEXT_PADDING
                )
            )
        else:
            return self._component(environment)


class Entry(Component):
    pass
