from wrapper.renderable import Renderable, Nothing
import pygame


class Scrap:
    """Base class for components of the app."""

    def cache(self) -> Renderable:
        return Nothing()

    def render(self, surface: pygame.Surface):
        self.cache().render(surface)
