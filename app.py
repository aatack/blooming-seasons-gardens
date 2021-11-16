from components import *
from structs import *
from window import Window
import settings
import pygame


@struct
class PlannerPosition(Point):
    def key(self, key: int, down: bool = True):
        if not down:
            return

        if key == pygame.K_a:
            self.x = self.x - 10
        elif key == pygame.K_d:
            self.x = self.x + 10
        elif key == pygame.K_w:
            self.y = self.y - 10
        elif key == pygame.K_s:
            self.y = self.y + 10


def app(window: Window, garden: State) -> State:
    editor_width = window.width * settings.EDITOR_WIDTH
    return Ordered(
        _editor(garden, editor_width, window.height),
        Offset(
            _planner(garden, window.width - editor_width, window.height), x=editor_width
        ),
    )


def _editor(garden: State, width: State, height: State) -> State:
    return Ordered(
        Rectangle(
            width=width,
            height=height,
            red=settings.EDITOR_BACKGROUND_BRIGHTNESS,
            blue=settings.EDITOR_BACKGROUND_BRIGHTNESS,
            green=settings.EDITOR_BACKGROUND_BRIGHTNESS,
        ),
        garden.editor(width),
    )


def _planner(garden: State, width: State, height: State) -> State:
    position = PlannerPosition(100, 100)

    planner = Peek(
        width,
        height,
        Offset(
            Offset(garden.planner(), x=-1 * position["x"], y=-1 * position["y"]),
            x=width * 0.5,
            y=height * 0.5,
        ),
    )
    planner.key = lambda *args, **kwargs: position.key(*args, **kwargs)
    return planner


@struct
class Plant(Point):
    name: str
    colour: Colour
    radius: float
    border: float

    @prepare
    def outer(radius: float, border: float) -> Circle:
        return Circle(radius=Derived(lambda r, b: r + b, radius, border))

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

    def editor(self, width: State) -> State:
        return Column(
            Text("Plant", 24),
            Text("Name: " + Derived(str, self["name"]), 12),
            Text("Radius: " + Derived(str, self["radius"]), 12),
        )

    def planner(self) -> State:
        colour = self["colour"]
        return Circle(
            self["radius"],
            red=colour["red"],
            green=colour["green"],
            blue=colour["blue"],
        )
