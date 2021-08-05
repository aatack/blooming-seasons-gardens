from scrap.base import Scrap
from scrap.data import Point, Colour
import wrapper.renderable as renderable
from typing import List
import pygame


class Box(Scrap):
    def __init__(self, top_left: Point, bottom_right: Point, colour: Colour):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.colour = colour

    def cache(self) -> renderable.Renderable:
        return renderable.Box(
            self.top_left.cache(), self.bottom_right.cache(), self.colour.cache()
        )


class Text(Scrap):
    def __init__(
        self, text: str, top_left: Point, size: int, font: str = "segoeuisemibold"
    ):
        self.text = text
        self.top_left = top_left
        self.size = size
        self.font = font

    def cache(self) -> renderable.Renderable:
        return renderable.Text(self.text, self.top_left.cache(), self.size, self.font)

    @staticmethod
    def list_available_fonts() -> List[str]:
        return pygame.font.get_fonts()


class Circle(Scrap):
    def __init__(self, centre: Point, radius: float, colour: Colour):
        self.centre = centre
        self.radius = radius
        self.colour = colour

    def cache(self) -> renderable.Renderable:
        return renderable.Circle(
            self.centre.cache(), int(self.radius), self.colour.cache()
        )
