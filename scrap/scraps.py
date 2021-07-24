from scrap.base import Scrap
import wrapper.renderable as renderable
from typing import List


class Point(Scrap):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def cache(self) -> renderable.Renderable:
        return renderable.Point(int(self.x), int(self.y))


class Group(Scrap):
    def __init__(self, *children: List[Scrap]):
        self.children = children

    def cache(self) -> renderable.Renderable:
        return renderable.Group(self.children)


class Colour(Scrap):
    def __init__(self, red: float = 0.0, green: float = 0.0, blue: float = 0.0):
        self.red = red
        self.green = green
        self.blue = blue

    def cache(self) -> renderable.Renderable:
        return renderable.Colour(
            int(self.red * 255), int(self.green * 255), int(self.blue * 255)
        )


class Circle(Scrap):
    def __init__(self, origin: Point, radius: float, colour: Colour):
        self.origin = origin
        self.radius = radius
        self.colour = colour

    def cache(self) -> renderable.Renderable:
        return renderable.Circle(
            self.origin.cache(), int(self.radius), self.colour.cache()
        )
