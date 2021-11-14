from components import *
from structs import *


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
