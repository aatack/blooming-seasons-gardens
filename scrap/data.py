from scrap.base import Scrap
import wrapper.renderable as renderable
from typing import List, Any
import pygame


class Literal(Scrap):
    def __init__(self, value: Any):
        self.value = value

    def __str__(self) -> str:
        return f"`{self.value}"


class Message(Scrap):
    def __init__(self, scrap: Scrap, message: Scrap):
        self.scrap = scrap
        self.message = message

        assert not isinstance(self.scrap, Message), "Nested message inside scrap"
        assert not isinstance(self.message, Message), "Nested message inside message"

    @staticmethod
    def collapse(scrap: Scrap, message: "Message") -> "Message":
        return Message(
            scrap, message.message if isinstance(message, Message) else message
        )

    def __str__(self) -> str:
        return f"Message(scrap={self.scrap}, message={self.message})"


class Point(Scrap):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def cache(self) -> renderable.Renderable:
        return renderable.Point(int(self.x), int(self.y))

    def left(self, change: float) -> "Point":
        return Point(self.x - change, self.y)

    def right(self, change: float) -> "Point":
        return Point(self.x + change, self.y)

    def up(self, change: float) -> "Point":
        return Point(self.x, self.y - change)

    def down(self, change: float) -> "Point":
        return Point(self.x, self.y + change)

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"


class Colour(Scrap):
    def __init__(self, red: float = 0.0, green: float = 0.0, blue: float = 0.0):
        self.red = red
        self.green = green
        self.blue = blue

    def cache(self) -> renderable.Renderable:
        return renderable.Colour(
            int(self.red * 255), int(self.green * 255), int(self.blue * 255)
        )

    def __str__(self) -> str:
        return f"Colour(red={self.red}, green={self.green}, blue={self.blue})"
