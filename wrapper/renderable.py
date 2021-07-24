import abc
import pygame
from typing import Tuple, List


class Renderable(abc.ABC):
    @abc.abstractmethod
    def render(self, surface: pygame.Surface):
        """Render this object to the given surface."""


class Nothing(Renderable):
    def render(self, surface: pygame.Surface):
        pass


class Point(Renderable):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def render(self, surface: pygame.Surface):
        pass

    def export(self) -> Tuple[int, int]:
        return self.x, self.y


class Colour(Renderable):
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def render(self, surface: pygame.Surface):
        surface.fill(self.export())

    def export(self) -> Tuple[int, int, int]:
        return self.red, self.green, self.blue


class Group(Renderable):
    def __init__(self, children: List[Renderable]):
        self.children = children

    def render(self, surface: pygame.Surface):
        for child in self.children:
            child.render(surface)


class Circle(Renderable):
    def __init__(self, origin: Point, radius: int, colour: Colour):
        self.origin = origin
        self.radius = radius
        self.colour = colour

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface, self.colour.export(), self.origin.export(), self.radius
        )
