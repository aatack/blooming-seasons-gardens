from typing import NamedTuple


class Colour(NamedTuple):
    red: int = 0
    blue: int = 0
    green: int = 0


WHITE = Colour(255, 255, 255)
BLACK = Colour(0, 0, 0)
