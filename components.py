from state import *
from structs import *
import pygame


@struct
class Colour:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    @derive
    def colour_cache(red: float, green: float, blue: float) -> tuple:
        return int(red * 255), int(green * 255), int(blue * 255)


@struct
class Point:
    x: float = 0.0
    y: float = 0.0

    @derive
    def point_cache(x: float, y: float) -> tuple:
        return int(x), int(y)


@struct
class Box:
    top: float = 0.0
    left: float = 0.0
    bottom: float = 0.0
    right: float = 0.0

    @derive
    def width(left: float, right: float) -> float:
        return right - left

    @derive
    def height(top: float, bottom: float) -> float:
        return bottom - top

    @derive
    def box_cache(top: float, left: float, width: float, height: float) -> tuple:
        return int(left), int(top), int(width), int(height)

    @prepare
    def top_left(top: float, left: float) -> Point:
        return Point(top, left)

    @prepare
    def bottom_right(bottom: float, right: float) -> Point:
        return Point(bottom, right)


@struct
class Rectangle(Colour):
    width: float
    height: float

    @prepare
    def box(width: float, height: float) -> Box:
        return Box(top=0.0, left=0.0, bottom=height, right=width)

    @derive
    def view(box: dict, colour_cache: tuple):
        box_cache = box["box_cache"]
        surface = pygame.Surface(box_cache[2:])
        pygame.draw.rect(surface, colour_cache, box_cache)
        return surface


@struct
class Circle(Point, Colour):
    radius: float = 0.0

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface, self.colour_cache, self.point_cache, int(self.radius)
        )


@struct
class Text:
    text: str
    size: int
    position: Point
    font: str = "segoeuisemibold"

    @derive
    def text_cache(text: str, size: int, font: str, position: dict) -> pygame.Surface:
        return pygame.font.SysFont(font, size).render(text, False, (0, 0, 0))

    def render(self, surface: pygame.Surface):
        surface.blit(self.text_cache, self["position"].point_cache)


@struct
class Plant:
    name: str
    position: Point
    colour: Colour
    radius: float
    border: float

    @prepare
    def outer(radius: float, border: float, position: dict) -> Circle:
        return Circle(
            radius=Derived(lambda r, b: r + b, radius, border),
            x=position["x"],
            y=position["y"],
        )

    @prepare
    def inner(radius: float, position: dict, colour: dict) -> Circle:
        return Circle(
            radius=radius,
            x=position["x"],
            y=position["y"],
            red=colour["red"],
            green=colour["green"],
            blue=colour["blue"],
        )

    @derive
    def text_x(position: dict, radius: float, border: float) -> float:
        return position["x"] + ((radius + border) * 0.8)

    @derive
    def text_y(position: dict, radius: float, border: float) -> float:
        return position["y"] + ((radius + border) * 0.8)

    @prepare
    def text(text_x: float, text_y: float, name: str) -> Text:
        return Text(text=name, size=12, position=Point(text_x, text_y,))

    def render(self, surface: pygame.Surface):
        self["outer"].render(surface)
        self["inner"].render(surface)
        self["text"].render(surface)


@struct
class Wrap:
    wrap: State

    def render(self, surface: pygame.Surface):
        self["wrap"].render(surface)


@struct
class Offset(Wrap):
    x: float = 0.0
    y: float = 0.0

    def render(self, surface: pygame.Surface):
        canvas = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
        canvas = canvas.convert_alpha()
        self["wrap"].render(canvas)
        surface.blit(canvas, (self.x, self.y))
