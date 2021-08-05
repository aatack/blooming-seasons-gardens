from wrapper.renderable import Renderable, Void
import pygame


class Scrap:
    """Base class for components of the app."""

    def cache(self) -> Renderable:
        """Return a cached version of the rendered view of this scrap."""
        return Void()

    def render(self, surface: pygame.Surface):
        """Render the scrap to a pygame surface."""
        self.cache().render(surface)

    def handle(self, event: "Scrap") -> "Scrap":
        return self
