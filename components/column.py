from typing import Callable, Optional, Tuple

from trickle.environment import Environment
from trickle.trickles.indexed import Folded, Indexed
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived
from trickle.visuals.overlay import Overlay
from trickle.visuals.reposition import Reposition
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


def column(
    environment: Environment,
    puddles: Indexed,
    build_visual: Callable[[Puddle, Environment], Puddle[Visual]],
) -> Puddle[Visual]:
    def function(
        current_state: Puddle[float], next_puddle: Puddle
    ) -> Tuple[Puddle, Puddle]:
        """
        Fold a puddle into a view of the puddle.

        The current state is the vertical offset of this puddle's visual from the top of
        the column component.  The next puddle will be the puddle whose view is going to
        be added to the column next.  The `build_visual` function will be called on the
        puddle, with an appropriately modified environment passed, to build a visual
        from the puddle.
        """
        modified_environment = environment.offset_mouse(
            vertical=current_state, horizontal=Constant(0.0), scale=Constant(1.0)
        )

        visual = build_visual(next_puddle, modified_environment)

        updated_state = Derived(
            lambda c, v: c + v.vertical_extent(), current_state, visual
        )
        repositioned_visual = Derived(
            lambda c, v: Reposition(v, vertical_offset=c), current_state, visual
        )

        return updated_state, repositioned_visual

    return Derived(
        lambda visuals: Overlay(*visuals),
        Folded(initial=Constant(0.0), function=function, indexed=puddles),
    )


def text_column(
    environment: Environment,
    puddles: Indexed,
    size: Puddle[int],
    padding: Optional[Puddle[int]] = None,
) -> Puddle[Visual]:
    if padding is None:
        padding = Constant(0)

    def build_visual(puddle: Puddle, _: Environment) -> Puddle[Visual]:
        return Derived(
            lambda v, s, p: Surface.text(str(v), s, padding=p), puddle, size, padding
        )

    return column(environment, puddles, build_visual)
