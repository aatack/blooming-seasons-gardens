import pygame
from typing import Tuple, Optional, Any
from scrap.base import Scrap
from scrap.scraps import *


class Window:
    def __init__(
        self,
        scrap: Scrap = Point(),
        width: int = 500,
        height: int = 500,
        background_colour: Colour = Colour(red=1.0, green=1.0, blue=1.0),
        title: Optional[str] = None,
    ):
        pygame.init()

        self.scrap = scrap
        self.cache = self.scrap.cache()

        self.surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        self.background_colour = background_colour.cache()

        self.title = title
        if self.title is not None:
            pygame.display.set_caption(self.title)

    def run(self):
        while self.loop():
            pass

    def loop(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.surface = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        self.background_colour.render(self.surface)

        # TODO: respond to any user events
        self.cache.render(self.surface)

        pygame.display.flip()
        return True
