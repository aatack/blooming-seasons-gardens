import pygame
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
        surface = Surface.empty(2 * radius, 2 * radius, transparent=True).surface

        radius = int(radius)
        colour = (int(red * 255), int(green * 255), int(blue * 255))

        pygame.draw.circle(surface, colour, (radius, radius), radius)

        return Surface(surface)

    @staticmethod
    def text(text: str, size: int, font: str = "segoeuisemibold") -> "Surface":
        return Surface(pygame.font.SysFont(font, size).render(text, False, (0, 0, 0)))

    def __init__(self, surface: pygame.Surface):
        self.surface = surface

    def simplify(self) -> "Visual":
        return Overlay(Reposition(self))

    def render(self, surface: pygame.Surface):
        surface.blit(self.surface, (0, 0))

    def horizontal_extent(self) -> float:
        return float(self.surface.get_size()[0])

    def vertical_extent(self) -> float:
        return float(self.surface.get_size()[1])
