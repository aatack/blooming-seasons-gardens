from typing import Callable, Dict, Type


class ScrapDispatch:

    ACTOR_ACTEE_DISPATCH = {}

    @classmethod
    def dispatch(cls, actor: str) -> Dict[str, Callable]:
        if actor not in cls.ACTOR_ACTEE_DISPATCH:
            cls.ACTOR_ACTEE_DISPATCH[actor] = {}
        return cls.ACTOR_ACTEE_DISPATCH[actor]

    @classmethod
    def register(cls, actor: str, actee: str, function: Callable):
        if actor not in cls.ACTOR_ACTEE_DISPATCH:
            cls.ACTOR_ACTEE_DISPATCH[actor] = {}
        cls.dispatch(actor)[actee] = function


def scrap(name: str) -> Callable:
    def decorator(constructor: Type) -> Type:
        return constructor

    return decorator


@scrap("translate")
class Translate:
    right: float
    down: float


@scrap("point")
class Point:
    x: float
    y: float

    def translate(self, translation: Translate) -> "Point":
        return Point(self.x + translation.right, self.y + translation.down)


@scrap("colour")
class Colour:
    red: int = 0
    green: int = 0
    blue: int = 0


@scrap("render_circle")
class RenderCircle:
    origin: Point
    radius: float
    colour: Colour

    def translate(self, translate: Translate) -> "RenderCircle":
        return RenderCircle(translate(self.origin), self.radius, self.colour)
