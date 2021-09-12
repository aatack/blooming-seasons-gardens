from scrap.base import defscrap, rebuild
from scrap.data import Point, Vector
from scrap.composite import Wrapper


@defscrap
class Key:
    # TODO: validation
    key: int
    down: bool = False
    up: bool = False


@defscrap
class Button(Point):
    # TODO: validation
    button: int
    x: float = 0.0
    y: float = 0.0
    down: bool = False
    up: bool = False


@defscrap
class Movement:
    start: Point
    end: Point

    def displacement(self) -> Vector:
        return Vector(self.end.x - self.start.x, self.end.y - self.start.y)

    def Translate(self, translation: ...) -> "Movement":
        return rebuild(self, start=self.start[translation], end=self.end[translation])

    def Scale(self, scale: ...) -> "Movement":
        return rebuild(self, start=self.start[scale], end=self.end[scale])


@defscrap
class Click(Point):
    button: int
    x: float = 0.0
    y: float = 0.0


@defscrap
class Start:
    pass


@defscrap
class Read:
    pass
