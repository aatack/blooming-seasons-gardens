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

    def where(self, **kwargs) -> "Environment":
        """Return a copy of the environment with some of its values changed."""
        return Environment(
            screen=kwargs.get("screen", self.screen),
            mouse=kwargs.get("mouse", self.mouse),
            keyboard=kwargs.get("keyboard", self.keyboard),
        )
