from scrap.base import Scrap
import wrapper.renderable as renderable
from typing import List
import pygame


class Point(Scrap):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def cache(self) -> renderable.Renderable:
        return renderable.Point(int(self.x), int(self.y))

    def left(self, change: float) -> "Point":
        return Point(self.x - change, self.y)

    def right(self, change: float) -> "Point":
        return Point(self.x + change, self.y)

    def up(self, change: float) -> "Point":
        return Point(self.x, self.y - change)

    def down(self, change: float) -> "Point":
        return Point(self.x, self.y + change)


class Colour(Scrap):
    def __init__(self, red: float = 0.0, green: float = 0.0, blue: float = 0.0):
        self.red = red
        self.green = green
        self.blue = blue

    def cache(self) -> renderable.Renderable:
        return renderable.Colour(
            int(self.red * 255), int(self.green * 255), int(self.blue * 255)
        )
