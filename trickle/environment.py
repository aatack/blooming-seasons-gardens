from dataclasses import dataclass
from typing import Optional

from trickle.trickles.interaction import Keyboard, Mouse, Screen
from trickle.trickles.log import Log


@dataclass
class Environment:
    """Stores trickles that broadcast user inputs."""

    screen: Screen
    mouse: Optional[Mouse] = None
    keyboard: Optional[Keyboard] = None

    def log(self, message: str = "Environment interaction:") -> Log:
        log = Log(
            message,
            predicate=lambda p, e: p != ("mouse",) or isinstance(e, Mouse.Click),
        )

        log.listen(("screen",), self.screen)
        if self.mouse is not None:
            log.listen(("mouse",), self.mouse)
        if self.keyboard is not None:
            log.listen(("keyboard",), self.keyboard)

        return log

    def offset_mouse(self, *args, **kwargs) -> "Environment":
        """Return a copy of the environment but with the mouse offset."""
        return Environment(
            screen=self.screen,
            mouse=self.mouse.offset(*args, **kwargs),
            keyboard=self.keyboard,
        )