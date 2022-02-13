import abc

import pygame


class Visual(abc.ABC):
    """
    Describes a purely visual component of an app.

    Development note: although objects with this general interface were originally
    conceived for speed/efficiency, the rework has not been done with that in mind.  See
    the tag `the-culling`, file `view.py` for an outline as to how this interface was
    achieved using simpler NamedTuple objects if performance ever does become an issue.
    """

    def simplify(self) -> "Visual":
        visual = self._simplify()

        assert visual.top() == self.top()
        assert visual.left() == self.left()
        assert visual.bottom() == self.bottom()
        assert visual.right() == self.right()

        return visual

    @abc.abstractmethod
    def _simplify(self) -> "Visual":
        """Simplify the structure of the visual where possible."""

    @abc.abstractmethod
    def render(self, surface: pygame.Surface):
        """
        Render the visual to a surface.

        This is allowed to not work properly if the view has not first been simplified.
        """

    @abc.abstractmethod
    def top(self) -> float:
        """Get the visual's maximum extent in the negative y-direction."""

    @abc.abstractmethod
    def left(self) -> float:
        """Get the visual's maximum extent in the negative x-direction."""

    @abc.abstractmethod
    def bottom(self) -> float:
        """Get the visual's maximum extent in the positive y-direction."""

    @abc.abstractmethod
    def right(self) -> float:
        """Get the visual's maximum extent in the positive x-direction."""

    def render_from_scratch(self, transparent: bool = False) -> pygame.Surface:
        from trickle.visuals.surface import Surface

        surface = Surface.empty(
            self.right(), self.bottom(), transparent=transparent
        ).surface
        self.render(surface)

        return surface
