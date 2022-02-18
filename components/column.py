from typing import Callable, List, Tuple, Union

from trickle import (
    Constant,
    Derived,
    Environment,
    Folded,
    Indexed,
    Overlay,
    Puddle,
    Surface,
    Visual,
)
from trickle import puddle as to_puddle

from components.component import Component
from components.positioning import Move


class Column(Component):
    def __init__(self, puddles: Indexed, get_component: Callable[[Puddle], Component]):
        super().__init__()

        self._puddles = puddles
        self._get_component = get_component

    def construct(self, environment: Environment):
        resized_environment = environment.where(
            screen=environment.screen.resize(height=None)
        )

        def function(
            current_state: Puddle[float], next_puddle: Puddle
        ) -> Tuple[Puddle, Puddle]:
            """
            Fold a puddle into a view of the puddle.

            The current state is the vertical offset of this puddle's visual from the
            top of the column component.  The next puddle will be the puddle whose
            component is going to be added to the column next.  The `get_component`
            function will be called on the puddle, and then an appropriately modified
            environment passed, to build a visual from the puddle.
            """
            repositioned_component = Move(
                self._get_component(next_puddle), vertical=current_state
            )
            repositioned_visual = repositioned_component(resized_environment)
            return repositioned_component.bottom, repositioned_visual

        self._visual = Derived(
            lambda visuals: Overlay(*visuals),
            Folded(initial=Constant(0.0), function=function, indexed=self._puddles),
        )

    def deconstruct(self):
        pass


class TextColumn(Column):
    def __init__(
        self, puddles: Indexed, size: Puddle[int], padding: Union[Puddle, int] = 0.0
    ):
        size = to_puddle(size)
        padding = to_puddle(padding)

        def get_component(puddle: Puddle) -> Component:
            return lambda _: Derived(
                lambda v, s, p: Surface.text(str(v), s, padding=p),
                puddle,
                size,
                padding,
            )

        super().__init__(puddles, get_component)


class ComponentColumn(Component):
    def __init__(self, *components: Component):
        super().__init__()

        self._components = components

    def construct(self, environment: Environment):
        visuals: List[Puddle] = []
        current_height = Constant(0.0)

        for component in self._components:
            assert isinstance(component, Component)
            moved = Move(component, vertical=current_height)
            visual = moved(environment)
            current_height = moved.bottom
            visuals.append(visual)

        self._visual = Derived(lambda v: Overlay(*v), Indexed(*visuals))

    def deconstruct(self):
        pass
