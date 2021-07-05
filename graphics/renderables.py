from typing import NamedTuple, Tuple
from graphics.colours import Colour
import pygame


Renderable = NamedTuple


class Group(Renderable):
    children: tuple

    def render(self, surface: pygame.Surface):
        for child in self.children:
            child.render(surface)

    def translate(self, x: int = 0, y: int = 0) -> Renderable:
        return Group(tuple(child.translate(x, y) for child in self.children))


class Point(Renderable):
    x: int
    y: int

    def render(self, surface: pygame.Surface):
        pass

    def translate(self, x: int = 0, y: int = 0) -> Renderable:
        return Point(self.x + x, self.y + y)


class Circle(Renderable):
    origin: Point
    radius: int
    colour: Colour

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.colour, self.origin, self.radius)

    def translate(self, x: int = 0, y: int = 0) -> Renderable:
        return Circle(self.origin.translate(x, y), self.radius, self.colour)
