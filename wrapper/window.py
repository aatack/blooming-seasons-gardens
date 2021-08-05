import pygame
from typing import Tuple, Optional, Any
from scrap.base import Scrap
from scrap.data import Point, Colour
from scrap.event import Key, MouseButton, MouseMovement


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
                _event = Key(event.key, down=True)
                self._update_cache(self.scrap.key_down(event.key))
            if event.type == pygame.KEYUP:
                _event = Key(event.key, up=True)
                self._update_cache(self.scrap.key_up(event.key))
            if event.type == pygame.MOUSEBUTTONDOWN:
                _event = MouseButton(event.button, Point(*event.pos), down=True)
                self._update_cache(
                    self.scrap.mouse_down(event.button, Point(*event.pos))
                )
            if event.type == pygame.MOUSEBUTTONUP:
                _event = MouseButton(event.button, Point(*event.pos), up=True)
                self._update_cache(self.scrap.mouse_up(event.button, Point(*event.pos)))
            if event.type == pygame.MOUSEMOTION:
                _event = MouseMovement(
                    Point(*event.pos),
                    Point(event.pos[0] - event.rel[0], event.pos[1] - event.rel[1]),
                )
                self._update_cache(
                    self.scrap.mouse_move(
                        Point(*event.pos),
                        Point(event.pos[0] - event.rel[0], event.pos[1] - event.rel[1]),
                    )
                )

        self.background_colour.render(self.surface)

        # TODO: respond to any user events
        self.cache.render(self.surface)

        pygame.display.flip()
        return True

    def _update_cache(self, scrap: Scrap):
        if scrap is not self.scrap:
            self.scrap = scrap
            self.cache = self.scrap.cache()
