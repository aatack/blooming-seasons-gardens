from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union

from trickle.trickles.keyed import Keyed
from trickle.trickles.puddle import Puddle, puddle
from trickle.trickles.singular import Derived, Variable
from trickle.trickles.trickle import Path, Trickle

_UNSPECIFIED = object()


class Screen(Keyed):
    def __init__(
        self,
        width: Union[Puddle[Optional[float]], Optional[float]],
        height: Union[Puddle[Optional[float]], Optional[float]],
    ):
        """
        Denotes the size of a screen.

        The width and height can also be given as None, in which case it is assumed that
        they should be determined by the content.  This is useful for things like a
        list of visual components whose widths are fixed but whose heights may vary.
        """
        self.width = puddle(width)
        self.height = puddle(height)

        super().__init__(width=self.width, height=self.height)

    def resize(
        self,
        width: Union[Puddle, Optional[float]] = _UNSPECIFIED,
        height: Union[Puddle, Optional[float]] = _UNSPECIFIED,
    ) -> "Screen":
        return Screen(
            width=self.width if width is _UNSPECIFIED else puddle(width),
            height=self.height if height is _UNSPECIFIED else puddle(height),
        )

    def shrink(self, amount: Union[Puddle, float]) -> "Screen":
        amount = puddle(amount)

        def shrink(_original: Optional[float], _amount: float) -> Optional[float]:
            if _original is None:
                return None
            return max(0, _original - _amount)

        return self.resize(
            width=Derived(shrink, self.width, amount),
            height=Derived(shrink, self.height, amount),
        )

    def contains_mouse(self, mouse: "Mouse") -> Puddle[bool]:
        def contains_mouse(
            width: Optional[float], height: Optional[float], x: float, y: float
        ) -> bool:
            return (
                x >= 0
                and ((width is None) or x < width)
                and y >= 0
                and ((height is None) or y < height)
            )

        return Derived(contains_mouse, self.width, self.height, mouse.x, mouse.y)


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

        self.click_listeners: Dict[Tuple[int, bool], List[Callable]] = {}

    def add_listener(self, button: int, down: bool, listener: Callable):
        pair = (button, down)
        if pair not in self.click_listeners:
            self.click_listeners[pair] = []
        self.click_listeners[pair].append(listener)

    def move(self, x: float, y: float):
        assert isinstance(self.x, Variable)
        self.x.change(x)

        assert isinstance(self.y, Variable)
        self.y.change(y)

    def click(self, button: int, down: bool):
        for listener in self.click_listeners.get((button, down), []):
            listener()
        self.broadcast(Mouse.Click(self.x.value(), self.y.value(), button, down))

    def respond(self, path: Path, event: Any):
        if path == ():
            if isinstance(event, Mouse.Click):
                # Rebroadcast click events; for offsetting mouse trickles (see below)
                self.click(event.button, event.down)
        else:
            super().respond(path, event)

    def offset(
        self,
        horizontal: Union[Puddle, float] = 0.0,
        vertical: Union[Puddle, float] = 0.0,
        scale: Union[Puddle, float] = 1.0,
    ):
        horizontal = puddle(horizontal)
        vertical = puddle(vertical)
        scale = puddle(scale)

        def transform(_position: float, _offset: float, _scale: float) -> float:
            return (_position - _offset) / _scale

        mouse = Mouse(
            Derived(transform, self.x, horizontal, scale),
            Derived(transform, self.y, vertical, scale),
        )

        mouse.listen((), self)
        return mouse


class Keyboard(Trickle):
    def __init__(self):
        super().__init__()

        self.key_listeners: Dict[Tuple[int, bool], List[Callable]] = {}

    class Key(NamedTuple):
        key: int
        down: bool

    def key(self, key: int, down: bool):
        for listener in self.key_listeners.get((key, down), []):
            listener()
        self.broadcast(Keyboard.Key(key, down))

    def respond(self, path: Path, event: Any):
        """Keyboards are sources of events, so have no responses."""
