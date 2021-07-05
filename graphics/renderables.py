from typing import NamedTuple, Tuple
from graphics.colours import Colour
import pygame
from math import cos, sin


Renderable = NamedTuple


class Group(Renderable):
    children: tuple

    def render(self, surface: pygame.Surface):
        for child in self.children:
            child.render(surface)

    def translate(self, x: float = 0.0, y: float = 0.0) -> Renderable:
        return Group(tuple(child.translate(x, y) for child in self.children))

    def rotate(self, radians: float) -> Renderable:
        return Group(tuple(child.rotate(radians) for child in self.children))


class Point(Renderable):
    x: int
    y: int

    def render(self, surface: pygame.Surface):
        pass

    def translate(self, x: float = 0.0, y: float = 0.0) -> Renderable:
        return Point(self.x + x, self.y + y)

    def rotate(self, radians: float) -> Renderable:
        cosine = cos(radians)
        sine = sin(radians)
        return Point(
            (self.x * cosine) - (self.y * sine), (self.y * cosine) + (self.x * sine)
        )


class Circle(Renderable):
    origin: Point
    radius: float
    colour: Colour

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            self.colour,
            (int(self.origin.x), int(self.origin.y)),
            int(self.radius),
        )

    def translate(self, x: float = 0.0, y: float = 0.0) -> Renderable:
        return Circle(self.origin.translate(x, y), self.radius, self.colour)

    def rotate(self, radians: float) -> Renderable:
        return Circle(self.origin.rotate(radians), self.radius, self.colour)
