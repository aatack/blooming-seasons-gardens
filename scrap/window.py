import pygame
from typing import Tuple, Optional, Any
from scrap.idea import Render, Colour, Circle, Void


class Window:
    def __init__(
        self,
        scrap: Any = Void(),
        width: int = 500,
        height: int = 500,
        background_colour: Colour = Colour(255, 255, 255),
        title: Optional[str] = None,
    ):
        pygame.init()
        self.render = Render()

        self.scrap = scrap
        self.cache = self.render(self.scrap)

        self.surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        self.background_colour = background_colour

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

        self.surface.fill(self.background_colour)

        # TODO: respond to any user events

        self.draw(self.scrap)

        pygame.display.flip()
        return True

    def draw(self, scrap: "Scrap"):
        if isinstance(scrap, Void):
            pass

        if isinstance(scrap, Circle):
            pygame.draw.circle(
                self.surface,
                scrap.colour,
                (int(scrap.origin.x), int(scrap.origin.y)),
                int(scrap.radius),
            )
