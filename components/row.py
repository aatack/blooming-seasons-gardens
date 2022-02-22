from typing import List, Optional

from trickle.environment import Environment
from trickle.trickles.indexed import Indexed
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived
from trickle.visuals.overlay import Overlay

from components.component import Component
from components.positioning import Move


class ComponentRow(Component):
    def __init__(self, *components: Component):
        super().__init__()

        self._components = components

        self._environment: Optional[Environment] = None
        self._width_internal: Optional[Puddle] = None

    def construct(self, environment: Environment):
        self._environment = environment

        resized_environment = environment.where(
            screen=environment.screen.resize(width=None)
        )

        visuals: List[Puddle] = []
        current_width = Constant(0.0)

        for component in self._components:
            assert isinstance(component, Component)
            moved = Move(component, horizontal=current_width)

            visual = moved(resized_environment)
            current_width = moved.width

            visuals.append(visual)

        self._width_internal = current_width
        self._visual = Derived(lambda v: Overlay(*v), Indexed(*visuals))

    def deconstruct(self):
        pass

    def _width(self) -> Puddle[float]:
        assert self._width_internal is not None
        return self._width_internal

    def _height(self) -> Puddle[float]:
        assert self._environment is not None
        return Derived(
            lambda e, *c: e if e is not None else max(c),
            self._environment.screen.height,
            *[component.height for component in self._components]
        )
