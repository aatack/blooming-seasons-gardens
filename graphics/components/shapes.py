from graphics.interfaces import *
from graphics.colours import Colour
from graphics.components.point import Point
import pygame


class Circle(Component):
    def __init__(self, origin: Point, radius: float, colour: Colour):
        self.origin = origin
        self.radius = radius
        self.colour = colour

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            self.colour,
            (int(self.origin.x), int(self.origin.y)),
            int(self.radius),
        )

    def translate(self, right: float = 0.0, down: float = 0.0) -> "Circle":
        self.origin = self.origin.translate(right, down)
        return self

    def rotate(self, turns_anticlockwise: float) -> "Circle":
        self.origin = self.origin.rotate(turns_anticlockwise)
        return self

    def scale(self, factor: float) -> "Circle":
        self.origin = self.origin.scale(factor)
        self.radius *= factor
        return self
