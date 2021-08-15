from scrap.base import defscrap
from scrap.data import Point, Colour, Message, Literal
from scrap.queries import Contains
import wrapper.renderable as renderable
from typing import List
import pygame


@defscrap
class Box:
    top_left: Point
    bottom_right: Point
    colour: Colour

    def _cache(self) -> renderable.Renderable:
        return renderable.Box(self.top_left(), self.bottom_right(), self.colour())

    def Contains(self, point: Point) -> Message:
        return Message(
            self,
            Literal(
                (self.top_left.x <= point.x <= self.bottom_right.x)
                and (self.top_left.y <= point.y <= self.bottom_right.y)
            ),
        )


@defscrap
class Text:
    text: str
    top_left: Point
    size: int
    font: str = "segoeuisemibold"

    def _cache(self) -> renderable.Renderable:
        return renderable.Text(self.text, self.top_left(), self.size, self.font)


def list_available_fonts() -> List[str]:
    return pygame.font.get_fonts()


@defscrap
class Circle:
    centre: Point
    radius: float
    colour: Colour

    def _cache(self) -> renderable.Renderable:
        return renderable.Circle(self.centre(), int(self.radius), self.colour())

    def Contains(self, point: Point) -> Message:
        return Message(
            self,
            Literal(
                (((self.centre.x - point.x) ** 2) + ((self.centre.y - point.y) ** 2))
                <= (self.radius ** 2)
            ),
        )
