import pygame
from typing import Tuple, Optional, Any
from state import State, view
from components import Colour


pygame.init()


class Window:
    def __init__(
        self,
        state: Optional[State] = None,
        width: int = 500,
        height: int = 500,
        background_colour: Colour = Colour(red=1.0, green=1.0, blue=1.0),
        title: Optional[str] = None,
    ):
        pygame.init()

        self.state = state
        self.view = view(state)
        self.background_colour = background_colour

        self.surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

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
                # self._update_cache(self.scrap.ResizeWindow(event.w, event.h))
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            #     self._update_cache(self.scrap.Key(event.key, down=True))
            # if event.type == pygame.KEYUP:
            #     self._update_cache(self.scrap.Key(event.key, up=True))
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     self._update_cache(
            #         self.scrap.Button(event.button, *event.pos, down=True)
            #     )
            # if event.type == pygame.MOUSEBUTTONUP:
            #     self._update_cache(self.scrap.Button(event.button, *event.pos, up=True))
            # if event.type == pygame.MOUSEMOTION:
            #     self._update_cache(
            #         self.scrap.Movement(
            #             Point(*event.pos),
            #             Point(event.pos[0] + event.rel[0], event.pos[1] + event.rel[1]),
            #         )
            #     )

        self.surface.fill(self.background_colour.colour_cache)
        if self.view is not None:
            view = self.view.value()
            if view is not None:
                self.surface.blit(view, (0, 0))

        pygame.display.flip()
        return True
