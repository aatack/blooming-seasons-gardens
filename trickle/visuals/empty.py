import pygame
from trickle.visuals.visual import Visual


class Empty(Visual):
    def __init__(self, visual: Visual):
        self._top = visual.top()
        self._left = visual.left()
        self._bottom = visual.bottom()
        self._right = visual.right()

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
