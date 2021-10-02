import pygame
from typing import Tuple, Optional, Any
from scrap.base import Scrap
from scrap.data import Point, Colour, Message
from scrap.event import Key, Button, Movement


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
        self.cache = self.scrap.Cache().message

        self.surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        self.background_colour = background_colour.Cache().message

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
                self._update_cache(self.scrap.Resize(event.w, event.h))
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                self._update_cache(self.scrap.Key(event.key, down=True))
            if event.type == pygame.KEYUP:
                self._update_cache(self.scrap.Key(event.key, up=True))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._update_cache(
                    self.scrap.Button(event.button, *event.pos, down=True)
                )
            if event.type == pygame.MOUSEBUTTONUP:
                self._update_cache(self.scrap.Button(event.button, *event.pos, up=True))
            if event.type == pygame.MOUSEMOTION:
                self._update_cache(
                    self.scrap.Movement(
                        Point(*event.pos),
                        Point(event.pos[0] + event.rel[0], event.pos[1] + event.rel[1]),
                    )
                )

        self.background_colour.Render(self.surface)
        self.cache.Render(self.surface)

        pygame.display.flip()
        return True

    def _update_cache(self, scrap: Scrap):
        if isinstance(scrap, Message):
            print(f"Message bubbled up: {scrap.message}")
            scrap = scrap.scrap

        if scrap is not self.scrap:
            self.scrap = scrap
            self.cache = self.scrap.Cache().message
