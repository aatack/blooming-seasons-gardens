from state import *
from structs import *
import pygame


"""
Wishlist:
-   Robust inheritance.  This should cover attributes, @derived, the construct described
    above, and then leave the leftovers to be handled by the normal python inheritance.
    But leave it for now, as most of this can be worked around - it's just a bit more
    cumbersome.
"""


@struct
class Colour:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    @derive
    def cache(red: float, green: float, blue: float) -> tuple:
        return int(red * 255), int(green * 255), int(blue * 255)

    def render(self, surface: pygame.Surface):
        surface.fill(self.cache)


@struct
class Point:
    x: float = 0.0
    y: float = 0.0


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
    def cache(top: float, left: float, width: float, height: float) -> tuple:
        return int(left), int(top), int(width), int(height)

    @prepare
    def top_left(top: float, left: float) -> Point:
        return Point(top, left)

    @prepare
    def bottom_right(bottom: float, right: float) -> Point:
        return Point(bottom, right)


@struct
class Rectangle:
    box: Box
    colour: Colour

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self["colour"].cache, self["box"].cache)