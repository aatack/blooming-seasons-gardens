from state import *
from structs import *
import pygame


@struct
class Colour:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    @derive
    def colour_cache(red: float, green: float, blue: float) -> tuple:
        return int(red * 255), int(green * 255), int(blue * 255)

    def render(self, surface: pygame.Surface):
        surface.fill(self.colour_cache)


@struct
class Point:
    x: float = 0.0
    y: float = 0.0

    @derive
    def point_cache(x: float, y: float) -> tuple:
        return int(x), int(y)


@struct
class Box:
    top: float = 0.0
    left: float = 0.0
    bottom: float = 0.0
    right: float = 0.0

    @derive
    def width(left: float, right: float) -> float:
        return right - left

    @derive
    def height(top: float, bottom: float) -> float:
        return bottom - top

    @derive
    def box_cache(top: float, left: float, width: float, height: float) -> tuple:
        return int(left), int(top), int(width), int(height)

    @prepare
    def top_left(top: float, left: float) -> Point:
        return Point(top, left)

    @prepare
    def bottom_right(bottom: float, right: float) -> Point:
        return Point(bottom, right)


@struct
class Rectangle(Box, Colour):
    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.colour_cache, self.box_cache)


@struct
class Circle(Point, Colour):
    radius: float = 0.0

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface, self.colour_cache, self.point_cache, int(self.radius)
        )


@struct
class Text:
    text: str
    size: int
    position: Point
    font: str = "segoeuisemibold"

    @derive
    def text_cache(text: str, size: int, font: str, position: dict) -> pygame.Surface:
        return pygame.font.SysFont(font, size).render(text, False, (0, 0, 0))

    def render(self, surface: pygame.Surface):
        surface.blit(self.text_cache, self["position"].point_cache)
