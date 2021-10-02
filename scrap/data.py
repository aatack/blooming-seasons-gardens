from scrap.base import defscrap, Scrap, rebuild
from typing import Any


@defscrap
class Literal:
    value: Any


@defscrap
class Message:
    # TODO: validation
    scrap: Scrap
    message: Scrap


@defscrap
class Vector:
    x: float = 0.0
    y: float = 0.0

    def Scale(self, scale: float) -> Scrap:
        return rebuild(self, x=self.x * scale, y=self.y * scale)

    def Cache(self) -> Message:
        from scrap.composite import Void

        return Message(self, Void())


@defscrap
class Point(Vector):
    def Translate(self, x: float, y: float) -> Scrap:
        return rebuild(self, x=self.x + x, y=self.y + y)

    def Render(self, render: ...) -> Scrap:
        return render

    def export(self) -> tuple:
        return int(self.x), int(self.y)


@defscrap
class Colour:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    def Render(self, render: ...) -> Scrap:
        render.surface.fill(self.export)
        return render

    def Cache(self) -> Message:
        return Message(self, self)

    def export(self) -> tuple:
        return int(self.red * 255), int(self.green * 255), int(self.blue * 255)
