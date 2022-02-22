from typing import Tuple

import pygame
import pygame.freetype
from pygame import gfxdraw
from trickle.visuals.empty import Empty
from trickle.visuals.visual import Visual


class Surface(Visual):
    class TooBig(Exception):
        def __init__(self, fallback: Visual):
            self.fallback = fallback

    @staticmethod
    def empty(width: float, height: float, transparent: bool = False) -> "Surface":
        try:
            if transparent:
                surface = pygame.Surface((int(width), int(height)), pygame.SRCALPHA)
            else:
                surface = pygame.Surface((int(width), int(height)))
            return Surface(surface)
        except pygame.error:
            raise Surface.TooBig(Empty(bottom=height, right=width))

    @staticmethod
    def circle(
        radius: float, red: float = 0.0, green: float = 0.0, blue: float = 0.0
    ) -> "Surface":
        # TODO: fix the harshness of circles

        try:
            surface = Surface.empty(2 * radius, 2 * radius, transparent=True).surface
        except Surface.TooBig as e:
            return e.fallback

        radius = int(radius)
        colour = (int(red * 255), int(green * 255), int(blue * 255))

        _draw_anti_aliased_circle(surface, colour, (radius, radius), radius)

        return Surface(surface)

    @staticmethod
    def text(
        text: str, size: int, font: str = "segoeuisemibold", padding: int = 0
    ) -> "Surface":
        system_font = pygame.freetype.SysFont(font, size)
        system_font.origin = True

        height = system_font.get_sized_height()
        bounds = system_font.get_rect(text)

        surface = Surface.empty(
            bounds.width + 4 + (2 * padding), height + (2 * padding), transparent=True
        ).surface

        system_font.render_to(
            surface, (2 + padding, int(height * 0.75) + padding), None
        )

        return Surface(surface)

    def __init__(self, surface: pygame.Surface, x: float = 0.0, y: float = 0.0):
        self.surface = surface
        self.x = x
        self.y = y

    def _simplify(self) -> "Visual":
        return self

    def render(self, surface: pygame.Surface):
        surface.blit(self.surface, (int(self.x), int(self.y)))

    def top(self) -> float:
        return self.y

    def left(self) -> float:
        return self.x

    def bottom(self) -> float:
        return self.y + float(self.surface.get_size()[1])

    def right(self) -> float:
        return self.x + float(self.surface.get_size()[0])


def _draw_anti_aliased_circle(
    surface: pygame.Surface,
    colour: Tuple[int, int, int],
    origin: Tuple[int, int],
    radius: int,
):
    gfxdraw.aacircle(surface, origin[0], origin[1], radius - 1, colour)
    gfxdraw.filled_circle(surface, origin[0], origin[1], radius - 1, colour)
