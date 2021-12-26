from typing import Any, NamedTuple, Optional

from trickle.trickles.keyed import Keyed
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Derived, Variable
from trickle.trickles.trickle import Path, Trickle


class Screen(Keyed):
    def __init__(self, width: Puddle[Optional[int]], height: Puddle[Optional[int]]):
        """
        Denotes the size of a screen.

        The width and height can also be given as None, in which case it is assumed that
        they should be determined by the content.  This is useful for things like a
        list of visual components whose widths are fixed but whose heights may vary.
        """
        super().__init__(width=width, height=height)

        self.width = width
        self.height = height

    def resize(self, width: Optional[int] = None, height: Optional[int] = None):
        assert isinstance(self.width, Variable)
        self.width.change(width)

        assert isinstance(self.height, Variable)
        self.height.change(height)


class Mouse(Keyed):
    # TODO: handle modifiers and utils for things like click to drag/offsetting

    class Click(NamedTuple):
        x: float
        y: float
        button: int
        down: bool

    def __init__(self, x: Puddle[float], y: Puddle[float]):
        """Denotes the position of the mouse."""
        super().__init__(x=x, y=y)

        self.x = x
        self.y = y

    def move(self, x: float, y: float):
        assert isinstance(self.x, Variable)
        self.x.change(x)

        assert isinstance(self.y, Variable)
        self.y.change(y)

    def click(self, button: int, down: bool):
        self.broadcast(Mouse.Click(self.x.value(), self.y.value(), button, down))

    def respond(self, path: Path, event: Any):
        if path == ():
            if isinstance(event, Mouse.Click):
                # Rebroadcast click events; for offsetting mouse trickles (see below)
                self.click(event.button, event.down)
        else:
            super().respond(path, event)

    def offset(
        self, horizontal: Puddle[float], vertical: Puddle[float], scale: Puddle[float]
    ):
        def transform(_position: float, _offset: float, _scale: float) -> float:
            return (_position - _offset) / _scale

        mouse = Mouse(
            Derived(transform, self.x, horizontal, scale),
            Derived(transform, self.y, vertical, scale),
        )

        mouse.listen((), self)
        return mouse


class Keyboard(Trickle):
    # TODO: handle modifiers

    class Key(NamedTuple):
        key: int
        down: bool

    def key(self, key: int, down: bool):
        self.broadcast(Keyboard.Key(key, down))

    def respond(self, path: Path, event: Any):
        """Keyboards are sources of events, so have no responses."""
