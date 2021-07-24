import abc
import pygame
from typing import List


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

        self.export = (self.x, self.y)

    def render(self, surface: pygame.Surface):
        pass


class Colour(Renderable):
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

        self.export = (self.red, self.green, self.blue)

    def render(self, surface: pygame.Surface):
        surface.fill(self.export)


class Group(Renderable):
    def __init__(self, children: List[Renderable]):
        self.children = children

    def render(self, surface: pygame.Surface):
        for child in self.children:
            child.render(surface)


class Box(Renderable):
    def __init__(self, top_left: Point, bottom_right: Point, colour: Colour):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.colour = colour

        self.export = (
            self.top_left.x,
            self.top_left.y,
            (self.bottom_right.x - self.top_left.x),
            (self.bottom_right.y - self.bottom_right.x),
        )

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.colour.export, self.export)


class Text(Renderable):
    def __init__(self, text: str, top_left: Point, size: int, font: str):
        self.text = text
        self.top_left = top_left
        self.size = size
        self.font = font

        self.export = pygame.font.SysFont(self.font, self.size).render(
            self.text, False, (0, 0, 0)
        )

    def render(self, surface: pygame.Surface):
        surface.blit(self.export, self.top_left.export)


class Circle(Renderable):
    def __init__(self, centre: Point, radius: int, colour: Colour):
        self.centre = centre
        self.radius = radius
        self.colour = colour

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.colour.export, self.centre.export, self.radius)
