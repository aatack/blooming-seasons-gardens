from scrap.base import defscrap, rebuild, Scrap
from scrap.data import Point, Colour, Message, Literal
from typing import List, Optional
import pygame


@defscrap
class Box:
    top_left: Point
    bottom_right: Point
    colour: Colour = Colour()

    def left(self) -> float:
        return self.top_left.x

    def top(self) -> float:
        return self.top_left.y

    def right(self) -> float:
        return self.bottom_right.x

    def bottom(self) -> float:
        return self.bottom_right.y

    def width(self) -> float:
        return self.right - self.left

    def height(self) -> float:
        return self.bottom - self.top

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

    def Cache(self) -> Message:
        return Message(self, self)

    def Bounds(self) -> Message:
        return Message(self, self)

    def Resize(self, width: Optional[float], height: Optional[float]) -> Scrap:
        return rebuild(
            self,
            bottom_right=Point(
                self.bottom_right.x if width is None else self.top_left.x + width,
                self.bottom_right.y if height is None else self.top_left.y + height,
            ),
        )


@defscrap
class Text:
    text: str
    size: int
    top_left: Point = Point()
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

    def Cache(self) -> Message:
        return Message(self, self)

    def Bounds(self) -> Message:
        return Message(
            self, Box(self.top_left, self.top_left.Translate(*self.export.get_size()))
        )

    def Contains(self, location: ...) -> Message:
        return self.Bounds().message[location]


def list_available_fonts() -> List[str]:
    return pygame.font.get_fonts()


@defscrap
class Circle:
    centre: Point
    radius: float
    colour: Colour = Colour()

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
        pygame.draw.circle(
            render.surface, self.colour.export, self.centre.export, int(self.radius)
        )
        return render

    def Cache(self) -> Message:
        return Message(self, self)

    def Bounds(self) -> Message:
        return Message(
            self,
            Box(
                self.centre.Translate(-self.radius, -self.radius),
                self.centre.Translate(self.radius, self.radius),
            ),
        )
