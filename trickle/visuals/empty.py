from typing import Optional

import pygame
from trickle.visuals.visual import Visual


class Empty(Visual):
    def __init__(
        self,
        visual: Optional[Visual] = None,
        *,
        top: float = 0.0,
        left: float = 0.0,
        bottom: float = 0.0,
        right: float = 0.0
    ):
        assert visual is None or isinstance(visual, Visual)
        self._top = visual.top() if visual is not None else top
        self._left = visual.left() if visual is not None else left
        self._bottom = visual.bottom() if visual is not None else bottom
        self._right = visual.right() if visual is not None else right

    def _simplify(self) -> "Visual":
        return self

    def render(self, surface: pygame.Surface):
        pass

    def top(self) -> float:
        return self._top

    def left(self) -> float:
        return self._left

    def bottom(self) -> float:
        return self._bottom

    def right(self) -> float:
        return self._right
