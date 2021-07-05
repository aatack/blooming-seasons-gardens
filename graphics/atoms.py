from typing import NamedTuple
import pygame


def render(atom: tuple, surface: pygame.Surface):
    if isinstance(atom, Circle):
        pygame.draw.circle(
            surface, atom.colour, (atom.horizontal, atom.vertical), atom.radius
        )
    elif isinstance(atom, tuple):
        for element in atom:
            render(element, surface)
    else:
        raise ValueError(f"Unrecognised atom: {atom}")


class Colour(NamedTuple):
    red: int = 0
    blue: int = 0
    green: int = 0


class Circle(NamedTuple):
    colour: Colour
    horizontal: int
    vertical: int
    radius: int
