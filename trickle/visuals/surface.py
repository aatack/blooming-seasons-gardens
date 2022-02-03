import pygame
import pygame.freetype
from trickle.visuals.overlay import Overlay
from trickle.visuals.reposition import Reposition
from trickle.visuals.visual import Visual


class Surface(Visual):
    @staticmethod
    def empty(width: float, height: float, transparent: bool = False) -> "Surface":
        if transparent:
            surface = pygame.Surface((int(width), int(height)), pygame.SRCALPHA)
        else:
            surface = pygame.Surface((int(width), int(height)))
        return Surface(surface)

    @staticmethod
    def rectangle(
        width: float,
        height: float,
        red: float = 0.0,
        green: float = 0.0,
        blue: float = 0.0,
    ) -> "Surface":
        surface = Surface.empty(width, height).surface

        rectangle = (0, 0, int(width), int(height))
        colour = (int(red * 255), int(green * 255), int(blue * 255))

        pygame.draw.rect(surface, colour, rectangle)
        return Surface(surface)

    @staticmethod
    def circle(
        radius: float, red: float = 0.0, green: float = 0.0, blue: float = 0.0
    ) -> "Surface":
        # TODO: fix the harshness of circles (and, actually, all other primitives)

        surface = Surface.empty(2 * radius, 2 * radius, transparent=True).surface

        radius = int(radius)
        colour = (int(red * 255), int(green * 255), int(blue * 255))

        pygame.draw.circle(surface, colour, (radius, radius), radius)

        return Surface(surface)

    @staticmethod
    def text(
        text: str, size: int, font: str = "segoeuisemibold", padding: int = 0
    ) -> "Surface":
        text_surface, *_ = pygame.freetype.SysFont(font, size).render(text)
        if padding != 0:
            width, height = text_surface.get_size()
            surface = Surface.empty(
                (2 * padding) + width, (2 * padding) + height, transparent=True
            ).surface
            surface.blit(text_surface, (padding, padding))
        else:
            surface = text_surface
        return Surface(surface)

    def __init__(self, surface: pygame.Surface, x: float = 0.0, y: float = 0.0):
        self.surface = surface
        self.x = x
        self.y = y

    def simplify(self) -> "Visual":
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
