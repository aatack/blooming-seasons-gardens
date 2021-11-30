import pygame

import view
from state import *
from structs import *


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

    def render(self, screen: Screen, mouse: Mouse, keyboard: Keyboard) -> Rendered:
        def _view(box: object, colour_cache: dict) -> view.View:
            box_cache = box.box_cache
            surface = view.empty(*box_cache[2:])
            pygame.draw.rect(surface, colour_cache, box_cache)
            return surface

        return Rendered(
            Derived(_view, self["box"], self["colour_cache"]),
            self,
            self["width"],
            self["height"],
        )


@struct
class Circle(Colour):
    radius: float = 0.0

    def render(self, screen: Screen, mouse: Mouse, keyboard: Keyboard) -> Rendered:
        def _view(radius: float, colour_cache: tuple) -> view.View:
            # TODO: make the circle appear central again
            draw_radius = int(radius)
            surface = view.empty(draw_radius * 2, draw_radius * 2, transparent=True)
            pygame.draw.circle(
                surface, colour_cache, (draw_radius, draw_radius), draw_radius
            )
            return view.Position(-draw_radius, -draw_radius, surface)

        return Rendered(
            Derived(_view, self["radius"], self["colour_cache"]),
            self,
            width=self["radius"],
            height=self["radius"],
        )


@struct
class Text:
    text: str
    size: int
    font: str = "segoeuisemibold"

    def render(self, screen: Screen, mouse: Mouse, keyboard: Keyboard) -> Rendered:
        return Rendered(
            Derived(
                lambda text, size, font: pygame.font.SysFont(font, size).render(
                    text, False, (0, 0, 0)
                ),
                self["text"],
                self["size"],
                self["font"],
            ),
            self,
        )


@struct
class Wrap:
    wrap: State

    def render(self, screen: Screen, mouse: Mouse, keyboard: Keyboard) -> Rendered:
        render = self["wrap"].render(screen, mouse, keyboard)
        return Rendered(render, self, width=render.width, height=render.height)


@struct
class Offset(Wrap):
    x: float = 0.0
    y: float = 0.0

    def render(self, screen: Screen, mouse: Mouse, keyboard: Keyboard) -> Rendered:
        offset_mouse = OffsetMouse(mouse, -1 * self["x"], -1 * self["y"])
        render = self["wrap"].render(screen, offset_mouse, keyboard)
        return Rendered(
            Derived(
                lambda _x, _y, _view: view.Position(_x, _y, _view),
                self["x"],
                self["y"],
                render,
            ),
            self,
        )


@struct
class Peek(Wrap):
    width: float
    height: float

    def render(self, screen: Screen, mouse: Mouse, keyboard: Keyboard) -> Rendered:
        render = self["wrap"].render(screen, mouse, keyboard)
        return Rendered(
            Derived(
                lambda _width, _height, _view: view.Peek(_width, _height, _view),
                self["width"],
                self["height"],
                render,
            ),
            self,
        )


class Column(Folded):
    def __init__(self, *children: Ordered):
        initial = Constant(0)

        def fold(current, child):
            return (
                current + Derived(view.height, Derived(view.simplify, child.view())),
                Offset(child, y=current),
            )

        super().__init__(initial, Ordered(*children), fold)


class Row(Folded):
    def __init__(self, *children: Ordered):
        initial = Constant(0)

        def fold(current, child):
            return (
                current + Derived(view.width, Derived(view.simplify, child.view())),
                Offset(child, x=current),
            )

        super().__init__(initial, Ordered(*children), fold)
