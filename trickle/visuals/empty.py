import pygame
from trickle.visuals.visual import Visual


class Empty(Visual):
    def simplify(self) -> "Visual":
        return self

    def render(self, surface: pygame.Surface):
        pass

    def top(self) -> float:
        return 0.0

    def left(self) -> float:
        return 0.0

    def bottom(self) -> float:
        return 0.0

    def right(self) -> float:
        return 0.0
