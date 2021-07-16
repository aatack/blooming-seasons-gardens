from typing import Callable, Dict, Type
from collections import namedtuple
import inspect


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


def scrap(actee: str) -> Callable:
    def decorator(constructor: Type) -> Type:
        definition = {k: v for k, v in inspect.getmembers(constructor)}

        fields = []
        defaults = []

        for field_name, field_type in definition.get("__annotations__", {}).items():
            fields.append(field_name)
            if len(defaults) > 0:
                assert field_name in definition
            if field_name in definition:
                defaults.append(definition[field_name])

        for actor, function in definition.items():
            if not actor.startswith("__") and actor not in fields:
                assert type(function).__name__ == "function"
                ScrapDispatch.register(actor, actee, function)

        modified_constructor = namedtuple(actee, fields, defaults=defaults)

        dispatch_dictionary = ScrapDispatch.dispatch(actee)

        def __call__(_actor, _actee):
            function = dispatch_dictionary.get(type(_actee).__name__, None)
            if function is not None:
                return function(_actee, _actor)
            else:
                return _actee

        setattr(modified_constructor, "__call__", __call__)
        return modified_constructor

    return decorator


@scrap("void")
class Void:
    pass


@scrap("render")
class Render:
    pass


@scrap("translate")
class Translate:
    right: float = 0.0
    down: float = 0.0


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


@scrap("circle")
class Circle:
    origin: Point
    radius: float
    colour: Colour

    def translate(self, translate: Translate) -> "RenderCircle":
        return RenderCircle(translate(self.origin), self.radius, self.colour)
