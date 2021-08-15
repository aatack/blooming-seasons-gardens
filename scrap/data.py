from scrap.base import defscrap, Scrap
import wrapper.renderable as renderable
from typing import Any


@defscrap
class Literal:
    value: Any


@defscrap
class Message:
    # TODO: validation
    scrap: Scrap
    message: Scrap


@defscrap
class Point:
    x: float = 0.0
    y: float = 0.0

    def _cache(self) -> renderable.Renderable:
        return renderable.Point(int(self.x), int(self.y))


@defscrap
class Colour:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    def _cache(self) -> renderable.Renderable:
        return renderable.Colour(
            int(self.red * 255), int(self.green * 255), int(self.blue * 255)
        )
