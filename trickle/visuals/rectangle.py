import pygame
from trickle.visuals.empty import Empty
from trickle.visuals.visual import Visual


class Rectangle(Visual):
    def __init__(
        self,
        *,
        width: float,
        height: float,
        x: float = 0.0,
        y: float = 0.0,
        red: float = 0.0,
        green: float = 0.0,
        blue: float = 0.0
    ):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.red = red
        self.green = green
        self.blue = blue

    def _simplify(self) -> "Visual":
        if self.width <= 0 or self.height <= 0:
            return Empty(self)
        else:
            return self

    def render(self, surface: pygame.Surface):
        rectangle = (int(self.x), int(self.y), int(self.width), int(self.height))
        colour = (int(self.red * 255), int(self.green * 255), int(self.blue * 255))

        pygame.draw.rect(surface, colour, rectangle)

    def top(self) -> float:
        return self.y

    def left(self) -> float:
        return self.x

    def bottom(self) -> float:
        return self.y + self.height

    def right(self) -> float:
        return self.x + self.width
