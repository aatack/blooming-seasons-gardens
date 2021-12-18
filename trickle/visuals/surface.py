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

    def __init__(self, surface: pygame.Surface):
        self.surface = surface

    def simplify(self) -> "Visual":
        return Overlay(Reposition(self))

    def render(self, surface: pygame.Surface):
        surface.blit(self.surface)

    def horizontal_extent(self) -> float:
        return float(self.surface.get_size()[0])

    def vertical_extent(self) -> float:
        return float(self.surface.get_size()[1])
