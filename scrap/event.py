from scrap.base import Scrap
from scrap.data import Point


class Key(Scrap):
    def __init__(self, key: int, down: bool = False, up: bool = False):
        self.key = key
        self.down = down
        self.up = up

        assert self.down is (not self.up)


class MouseButton(Scrap):
    def __init__(
        self, button: int, location: Point, down: bool = False, up: bool = False
    ):
        self.button = button
        self.location = location
        self.down = down
        self.up = up

        assert self.down is (not self.up)


class MouseMovement(Scrap):
    def __init__(self, before: Point, after: Point):
        self.before = before
        self.after = after
