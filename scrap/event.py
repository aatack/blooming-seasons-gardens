from scrap.base import Scrap
from scrap.data import Point


class Key(Scrap):
    def __init__(self, key: int, down: bool = False, up: bool = False):
        self.key = key
        self.down = down
        self.up = up

        assert self.down is (not self.up)

    def __str__(self) -> str:
        return f"Key(key={self.key}, down={self.down}, up={self.up})"


class Button(Scrap):
    def __init__(
        self, button: int, location: Point, down: bool = False, up: bool = False
    ):
        self.button = button
        self.location = location
        self.down = down
        self.up = up

        assert self.down is (not self.up)

    def __str__(self) -> str:
        return (
            f"Button(button={self.button}, location={self.location}, "
            f"up={self.up}, down={self.down})"
        )


class Movement(Scrap):
    def __init__(self, beginning: Point, end: Point):
        self.beginning = beginning
        self.end = end

    @property
    def displacement(self) -> Point:
        return Point(self.end.x - self.beginning.x, self.end.y - self.beginning.y)

    def __str__(self) -> str:
        return f"Movement(beginning={self.beginning}, end={self.end})"


class Click(Scrap):
    def __init__(self, button: int, location: Point):
        self.button = button
        self.location = location

    def __str__(self) -> str:
        return f"Click(button={self.button}, location={self.location})"
