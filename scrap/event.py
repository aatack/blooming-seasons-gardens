from scrap.base import defscrap
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
        return self.wrao


@defscrap
class Movement:
    start: Point
    end: Point

    def displacement(self) -> Vector:
        return Vector(self.end.x - self.start.x, self.end.y - self.start.y)


@defscrap
class Click:
    button: int
    location: Point


@defscrap
class Start:
    pass


@defscrap
class Read:
    pass
