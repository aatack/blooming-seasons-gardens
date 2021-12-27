from typing import Callable, Optional, Tuple

from trickle import (
    Constant,
    Derived,
    Environment,
    Folded,
    Indexed,
    Overlay,
    Puddle,
    Reposition,
    Surface,
    Visual,
)

from components.component import Component


class Column(Component):
    def __init__(self, puddles: Indexed, get_component: Callable[[Puddle], Component]):
        self._puddles = puddles
        self._get_component = get_component

    def __call__(self, environment: Environment) -> Puddle[Visual]:
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
            modified_environment = environment.offset_mouse(vertical=current_state)

            visual = self._get_component(next_puddle)(modified_environment)

            updated_state = Derived(
                lambda c, v: c + v.vertical_extent(), current_state, visual
            )
            repositioned_visual = Derived(
                lambda c, v: Reposition(v, vertical_offset=c), current_state, visual
            )

            return updated_state, repositioned_visual

        return Derived(
            lambda visuals: Overlay(*visuals),
            Folded(initial=Constant(0.0), function=function, indexed=self._puddles),
        )


class TextColumn(Column):
    def __init__(
        self, puddles: Indexed, size: Puddle[int], padding: Optional[Puddle[int]] = None
    ):
        if padding is None:
            padding = Constant(0)

        def get_component(puddle: Puddle) -> Component:
            return lambda _: Derived(
                lambda v, s, p: Surface.text(str(v), s, padding=p),
                puddle,
                size,
                padding,
            )

        super().__init__(puddles, get_component)
