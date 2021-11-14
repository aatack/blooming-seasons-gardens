from state import *
from structs import *
import pygame
import view


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
    def view(box: dict, colour_cache: tuple) -> view.View:
        box_cache = box["box_cache"]
        surface = view.empty(*box_cache[2:])
        pygame.draw.rect(surface, colour_cache, box_cache)
        return surface


@struct
class Circle(Colour):
    radius: float = 0.0

    @derive
    def view(radius: float, colour_cache: tuple) -> view.View:
        # TODO: offset by (-radius, -radius)
        draw_radius = int(radius)
        surface = view.empty(draw_radius * 2, draw_radius * 2, transparent=True)
        pygame.draw.circle(
            surface, colour_cache, (draw_radius, draw_radius), draw_radius
        )
        return surface


@struct
class Text:
    text: str
    size: int
    font: str = "segoeuisemibold"

    @derive
    def view(text: str, size: int, font: str) -> view.View:
        return pygame.font.SysFont(font, size).render(text, False, (0, 0, 0))


@struct
class Plant:
    name: str
    colour: Colour
    radius: float
    border: float

    @prepare
    def outer(radius: float, border: float) -> Circle:
        return Circle(radius=Derived(lambda r, b: r + b, radius, border),)

    @prepare
    def inner(radius: float, colour: dict, border: float) -> Circle:
        return Offset(
            Circle(
                radius=radius,
                red=colour["red"],
                green=colour["green"],
                blue=colour["blue"],
            ),
            x=border,
            y=border,
        )

    @derive
    def text_x(radius: float, border: float) -> float:
        return (radius + border) * 1.8

    @derive
    def text_y(radius: float, border: float) -> float:
        return (radius + border) * 1.8

    @prepare
    def text(text_x: float, text_y: float, name: str) -> Text:
        return Offset(Text(text=name, size=12), x=text_x, y=text_y,)

    @prepare
    def view(outer: State, inner: State, text: State) -> State:
        return Derived(
            lambda _outer, _inner, _text: [_outer, _inner, _text],
            outer.view(),
            inner.view(),
            text.view(),
        )


@struct
class Wrap:
    wrap: State

    @prepare
    def view(wrap: State) -> State:
        return wrap["view"]

    def key(self, key: int, down: bool):
        self["wrap"].key(key, down)

    def mouse(self, button: int, position: Tuple[int, int], down: bool):
        self["wrap"].mouse(button, position, down)


@struct
class Offset(Wrap):
    x: float = 0.0
    y: float = 0.0

    @prepare
    def view(x: float, y: float, wrap: State) -> State:
        return Derived(lambda _x, _y, _view: (_x, _y, _view), x, y, wrap.view())

    def mouse(self, button: int, position: Tuple[int, int], down: bool):
        self["wrap"].mouse(
            button, (position[0] - self.x, position[1] - self.y), down,
        )
