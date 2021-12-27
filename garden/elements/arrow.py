from typing import Union

import pygame
from garden.element import Element
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle.components.column import text_column
from trickle.environment import Environment
from trickle.trickles.indexed import Indexed
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


class Arrow(Element):
    def __init__(
        self,
        start_horizontal: Union[float, Puddle],
        start_vertical: Union[float, Puddle],
        end_horizontal: Union[float, Puddle],
        end_vertical: Union[float, Puddle],
        width: Union[float, Puddle] = 3,
    ):
        super().__init__(
            start_horizontal=start_horizontal,
            start_vertical=start_vertical,
            end_horizontal=end_horizontal,
            end_vertical=end_vertical,
            width=width,
        )

    @property
    def start_horizontal(self) -> Puddle:
        return self["start_horizontal"]

    @property
    def start_vertical(self) -> Puddle:
        return self["start_vertical"]

    @property
    def end_horizontal(self) -> Puddle:
        return self["end_horizontal"]

    @property
    def end_vertical(self) -> Puddle:
        return self["end_vertical"]

    @property
    def width(self) -> Puddle:
        return self["width"]

    def plan(self, environment: Environment) -> Puddle:
        def plan(
            start_horizontal: float,
            start_vertical: float,
            end_horitonzal: float,
            end_vertical: float,
            width: float,
        ) -> Visual:
            surface = Surface.empty(
                max(0, start_horizontal, end_horitonzal) * SCALE,
                max(0, start_vertical, end_vertical) * SCALE,
                transparent=True,
            )
            pygame.draw.line(
                surface.surface,
                (0, 0, 0),
                (int(start_horizontal * SCALE), int(start_vertical * SCALE)),
                (int(end_horitonzal * SCALE), int(end_vertical * SCALE)),
                int(width),
            )
            return surface

        return Derived(
            plan,
            self.start_horizontal,
            self.start_vertical,
            self.end_horizontal,
            self.end_vertical,
            self.width,
        )

    def editor(self, environment: Environment) -> Puddle:
        return text_column(
            environment,
            Indexed(
                Constant("Arrow"),
                "Start: ("
                + Derived(str, self.start_horizontal)
                + ", "
                + Derived(str, self.start_vertical)
                + ")",
                "End: ("
                + Derived(str, self.end_horizontal)
                + ", "
                + Derived(str, self.end_vertical)
                + ")",
            ),
            Constant(16),
            padding=Constant(5),
        )
