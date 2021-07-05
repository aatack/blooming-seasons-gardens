import pygame
from typing import Tuple


class Window:
    def __init__(
        self,
        width: int = 500,
        height: int = 500,
        background_colour: Tuple[int, int, int] = (255, 255, 255),
    ):
        pygame.init()

        self.surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.background_colour = background_colour

    def loop(self, atom: tuple) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.surface = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
            if event.type == pygame.QUIT:
                return False

        self.surface.fill(self.background_colour)
        atom.render(self.surface)

        return True
