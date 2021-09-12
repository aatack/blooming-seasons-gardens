from scrap.base import defscrap, rebuild
from scrap.data import Point, Colour, Message, Literal
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

    def Contains(self, x: float, y: float) -> Message:
        return Message(
            self,
            Literal(
                (self.top_left.x <= x <= self.bottom_right.x)
                and (self.top_left.y <= y <= self.bottom_right.y)
            ),
        )

    def Translate(self, translation: ...) -> "Box":
        return rebuild(
            self,
            top_left=self.top_left[translation],
            bottom_right=self.bottom_right[translation],
        )

    def Scale(self, scale: ...) -> "Box":
        return rebuild(
            self, top_left=self.top_left[scale], bottom_right=self.bottom_right[scale]
        )


@defscrap
class Text:
    text: str
    top_left: Point
    size: int
    font: str = "segoeuisemibold"

    def _cache(self) -> renderable.Renderable:
        return renderable.Text(self.text, self.top_left(), self.size, self.font)

    def Translate(self, translation: ...) -> "Text":
        return rebuild(self, top_left=self.top_left[translation])

    def Scale(self, scale: float) -> "Text":
        raise NotImplementedError("Cannot currently scale text")


def list_available_fonts() -> List[str]:
    return pygame.font.get_fonts()


@defscrap
class Circle:
    centre: Point
    radius: float
    colour: Colour

    def _cache(self) -> renderable.Renderable:
        return renderable.Circle(self.centre(), int(self.radius), self.colour())

    def Contains(self, x: float, y: float) -> Message:
        return Message(
            self,
            Literal(
                (((self.centre.x - x) ** 2) + ((self.centre.y - y) ** 2))
                <= (self.radius ** 2)
            ),
        )

    def Translate(self, translation: ...) -> "Circle":
        return rebuild(self, centre=self.centre[translation])

    def Scale(self, scale: float) -> "Circle":
        return rebuild(
            self, centre=self.centre.Scale(scale), radius=self.radius * scale
        )
