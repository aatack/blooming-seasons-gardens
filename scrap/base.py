from scrap.geometry import Point
from scrap.colours import Colour
import pygame


class Scrap:
    def __call__(self, scrap: "Scrap") -> "Scrap":
        return self


class Transform(Scrap):
    def inverse(self) -> "Scrap":
        raise NotImplementedError()


class Translate(Transform):
    def __init__(self, right: float, down: float):
        self.right = right
        self.down = down

    def inverse(self) -> "Translation":
        return Translation(-self.x, -self.y)


class Decompose(Scrap):
    pass


class Render(Scrap):
    def render(self, surface: pygame.Surface):
        raise NotImplementedError()


class RenderCircle(Render):
    def __init__(self, origin: Point, radius: float, colour: Colour):
        self.origin = origin
        self.radius = radius
        self.colour = colour

    def __call__(self, scrap: Scrap) -> "RenderCircle":
        if isinstance(scrap, Translate):
            return RenderCircle(
                self.origin.translate(scrap.right, scrap.down), self.radius, self.colour
            )
        return self


class Middleware(Scrap):
    def __init__(self, before: Scrap, wrapped: Scrap, after: Scrap):
        self.before = before
        self.wrapped = wrapped
        self.after = after

    def __call__(self, scrap: Scrap) -> Scrap:
        return self.after(self.before(scrap)(self.wrapped))
