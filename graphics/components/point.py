from typing import NamedTuple
from math import pi, cos, sin


class Point(NamedTuple):
    x: float
    y: float

    def translate(self, right: float = 0.0, down: float = 0.0) -> "Point":
        return Point(self.x + right, self.y + down)

    def rotate(self, turns_anticlockwise: float) -> "Point":
        # TODO: efficient cases for common turns (ie. half turn, quarter turn)
        radians = turns_anticlockwise * 2 * pi
        cosine = cos(radians)
        sine = sin(radians)
        return Point(
            (self.x * cosine) - (self.y * sine), (self.y * cosine) + (self.x * sine)
        )

    def scale(self, factor: float) -> "Point":
        return Point(self.x * factor, self.y * factor)

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"
