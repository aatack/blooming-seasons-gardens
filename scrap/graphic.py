from scrap.base import defscrap, rebuild, Scrap
from scrap.data import Point, Colour, Message, Literal
from typing import List
import pygame


@defscrap
class Box:
    top_left: Point
    bottom_right: Point
    colour: Colour

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

    def export(self) -> tuple:
        return (
            int(self.top_left.x),
            int(self.top_left.y),
            int(self.bottom_right.x - self.top_left.x),
            int(self.bottom_right.y - self.top_left.y),
        )

    def Render(self, render: ...) -> Scrap:
        pygame.draw.rect(render.surface, self.colour.export, self.export)
        return render


@defscrap
class Text:
    text: str
    top_left: Point
    size: int
    font: str = "segoeuisemibold"

    def Translate(self, translation: ...) -> "Text":
        return rebuild(self, top_left=self.top_left[translation])

    def Scale(self, scale: float) -> "Text":
        raise NotImplementedError("Cannot currently scale text")

    def export(self) -> pygame.Surface:
        return pygame.font.SysFont(self.font, self.size).render(
            self.text, False, (0, 0, 0)
        )

    def Render(self, render: ...) -> Scrap:
        render.surface.blit(self.export, self.top_left.export)
        return render


def list_available_fonts() -> List[str]:
    return pygame.font.get_fonts()


@defscrap
class Circle:
    centre: Point
    radius: float
    colour: Colour

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

    def Render(self, render: ...) -> Scrap:
        pyhame.draw.circle(
            render.surface, self.colour.export, self.centre.export, int(self.radius)
        )
        return render
