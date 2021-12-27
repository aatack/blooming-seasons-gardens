from typing import Callable

from trickle.environment import Environment
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Derived
from trickle.visuals.overlay import Overlay
from trickle.visuals.reposition import Reposition
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


def card(
    build_visual: Callable[[Puddle, Environment], Puddle[Visual]],
    colour: tuple,
    border: int,
    *args,
    **kwargs
) -> Callable[[Puddle, Environment], Puddle[Visual]]:
    def _card(puddle: Puddle, environment: Environment) -> Puddle[Visual]:
        return Derived(
            lambda v: Reposition(
                Overlay(
                    Reposition(
                        Surface.rectangle(
                            v.horizontal_extent(),
                            v.vertical_extent(),
                            red=colour[0],
                            green=colour[1],
                            blue=colour[2],
                        ),
                        crop_left=-border,
                        crop_right=v.horizontal_extent() + border,
                        crop_top=-border,
                        crop_bottom=v.vertical_extent() + border,
                    ),
                    v,
                ),
                horizontal_offset=border,
                vertical_offset=border,
            ),
            build_visual(puddle, environment, *args, **kwargs),
        )

    return _card
