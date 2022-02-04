import pygame
from trickle.visuals.visual import Visual


class Empty(Visual):
    def __init__(
        self,
        top: float = 0.0,
        left: float = 0.0,
        bottom: float = 0.0,
        right: float = 0.0,
    ):
        self._top = top
        self._left = left
        self._bottom = bottom
        self._right = right

    def simplify(self) -> "Visual":
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
