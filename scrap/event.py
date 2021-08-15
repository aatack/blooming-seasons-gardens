from scrap.base import defscrap
from scrap.data import Point


@defscrap
class Key:
    # TODO: validation
    key: int
    down: bool = False
    up: bool = False


@defscrap
class Button:
    # TODO: validation
    button: int
    location: Point
    down: bool = False
    up: bool = False


@defscrap
class Movement:
    start: Point
    end: Point

    def displacement(self) -> Point:
        return Point(self.end.x - self.start.x, self.end.y - self.start.y)


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
