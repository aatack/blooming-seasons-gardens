from typing import NamedTuple, Tuple
from graphics.colours import Colour
import pygame


class Group(NamedTuple):
    children: tuple

    def render(self, surface: pygame.Surface):
        for child in self.children:
            child.render(surface)


class Circle(NamedTuple):
    horizontal: int
    vertical: int
    radius: int
    colour: Colour

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface, self.colour, (self.horizontal, self.vertical), self.radius
        )
