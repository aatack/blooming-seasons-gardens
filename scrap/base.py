from wrapper.renderable import Renderable, Nothing
import pygame


class Scrap:
    """Base class for components of the app."""

    def cache(self) -> Renderable:
        """Return a cached version of the rendered view of this scrap."""
        return Nothing()

    def render(self, surface: pygame.Surface):
        """Render the scrap to a pygame surface."""
        self.cache().render(surface)

    def key_down(self, key: int) -> "Scrap":
        """
        Respond to a key being pressed.

        The key is identified by its pygame enum.  If the scrap does not do anything in
        response to the key press, it may return itself.
        """
        return self

    def key_up(self, key: int) -> "Scrap":
        """
        Respond to a key being released.

        The key is identified by its pygame enum.  If the scrap does not do anything in
        response to the key release, it may return itself.
        """
        return self

    def mouse_down(self, button: int, location: "Point") -> "Scrap":
        """Respond to a mouse button being pressed at the given location."""
        return self

    def mouse_up(self, button: int, location: "Point") -> "Scrap":
        """Respond to a mouse button being pressed at the given location."""
        return self

    def mouse_move(self, before: "Point", after: "Point") -> "Scrap":
        """Respond to a relative mouse movement."""
