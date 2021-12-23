from typing import NamedTuple, Optional

from trickle import Keyboard, Mouse, Screen


class Environment(NamedTuple):
    """Stores trickles that broadcast user inputs."""

    screen: Screen
    mouse: Optional[Mouse] = None
    keyboard: Optional[Keyboard] = None
