from typing import Union

import pygame
from components.column import TextColumn
from components.component import Component
from components.presentation import Card
from garden.element import Element
from settings import (
    EDITOR_BLOCK_COLOUR,
    EDITOR_PADDING,
    EDITOR_TEXT_PADDING,
    EDITOR_TEXT_SIZE,
)
from settings import PIXELS_PER_DISTANCE_UNIT as SCALE
from trickle import Constant, Derived, Environment, Indexed, Puddle, Surface, Visual


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

    @property
    def plan(self) -> Component:
        return Arrow.Plan(self)

    @property
    def editor(self) -> Component:
        return Arrow.Editor(self)

    class Plan(Component):
        def __init__(self, arrow: "Arrow"):
            super().__init__()

            self._arrow = arrow

        @staticmethod
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

        def construct(self, environment: Environment):
            self._visual = Derived(
                self.plan,
                self._arrow.start_horizontal,
                self._arrow.start_vertical,
                self._arrow.end_horizontal,
                self._arrow.end_vertical,
                self._arrow.width,
            )

            # TODO: check this environment is correct
            self._environment = environment

        def deconstruct(self):
            pass

    class Editor(Component):
        def __init__(self, arrow: "Arrow"):
            super().__init__()

            self._arrow = arrow

        def construct(self, environment: Environment):
            puddles = Indexed(
                Constant("Arrow"),
                "Start: ("
                + Derived(str, self._arrow.start_horizontal)
                + ", "
                + Derived(str, self._arrow.start_vertical)
                + ")",
                "End: ("
                + Derived(str, self._arrow.end_horizontal)
                + ", "
                + Derived(str, self._arrow.end_vertical)
                + ")",
            )
            self._visual = Card(
                TextColumn(
                    puddles,
                    Constant(EDITOR_TEXT_SIZE),
                    padding=Constant(EDITOR_TEXT_PADDING),
                ),
                EDITOR_BLOCK_COLOUR,
                EDITOR_PADDING,
            )(environment)

            # TODO: check this environment is correct
            self._environment = environment

        def deconstruct(self):
            pass
