from typing import Union

from trickle import Derived, Environment, Puddle, Reposition, Visual, puddle

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
