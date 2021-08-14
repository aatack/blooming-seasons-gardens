from scrap.base import Scrap
from scrap.data import Point


class Key(Scrap):
    def __init__(self, key: int, down: bool = False, up: bool = False):
        self.key = key
        self.down = down
        self.up = up

        assert self.down is (not self.up)


class Button(Scrap):
    def __init__(
        self, button: int, location: Point, down: bool = False, up: bool = False
    ):
        self.button = button
        self.location = location
        self.down = down
        self.up = up

        assert self.down is (not self.up)


class Movement(Scrap):
    def __init__(self, beginning: Point, end: Point):
        self.beginning = beginning
        self.end = end

    @property
    def displacement(self) -> Point:
        return Point(self.end.x - self.beginning.x, self.end.y - self.beginning.y)
