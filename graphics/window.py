import pygame
from typing import Tuple, Optional


class Window:
    def __init__(
        self,
        width: int = 500,
        height: int = 500,
        background_colour: Tuple[int, int, int] = (255, 255, 255),
        title: Optional[str] = None,
    ):
        pygame.init()

        self.surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        self.background_colour = background_colour

        self.title = title
        if self.title is not None:
            pygame.display.set_caption(self.title)

    def loop(self, renderable: tuple) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.surface = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
            if event.type == pygame.QUIT:
                return False

        self.surface.fill(self.background_colour)
        renderable.render(self.surface)

        return True
