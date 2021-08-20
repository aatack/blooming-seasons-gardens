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
class Button(Wrapper):
    # TODO: validation
    wrap: Point
    button: int
    down: bool = False
    up: bool = False

    def location(self) -> Point:
        return self.wrap


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
class Click:
    wrap: Point
    button: int

    def location(self) -> Point:
        return self.wrap


@defscrap
class Start:
    pass


@defscrap
class Read:
    pass
