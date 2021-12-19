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

    @abc.abstractmethod
    def simplify(self) -> "Visual":
        """
        Simplify the structure of the visual where possible.
        
        The simplified visual must be an overlay containing repositions, each of which
        contains a surface.
        """

    @abc.abstractmethod
    def render(self, surface: pygame.Surface):
        """
        Render the visual to a surface.
        
        This is allowed to not work properly if the view has not first been simplified.
        """

    @abc.abstractmethod
    def horizontal_extent(self) -> float:
        """Get the visual's maximum extent in the positive x-direction."""

    @abc.abstractmethod
    def vertical_extent(self) -> float:
        """Get the visual's maximum extent in the negative y-direction."""

    def assert_simplified(self: "Visual"):
        from trickle.visuals.overlay import Overlay

        assert isinstance(
            self, Overlay
        ), "Simplified visuals must have an overlay at their top level"

        from trickle.visuals.reposition import Reposition
        from trickle.visuals.surface import Surface

        for child in self.visuals:
            assert isinstance(child, Reposition), (
                "Each child of the outer overlay in a simplified visual must be a "
                "reposition"
            )
            assert isinstance(
                child.visual, Surface
            ), "Each leaf in a simplified visual must be a surface"

    def render_from_scratch(self, transparent: bool = False) -> pygame.Surface:
        from trickle.visuals.surface import Surface

        surface = Surface.empty(
            self.horizontal_extent(), self.vertical_extent(), transparent=transparent
        ).surface
        self.render(surface)

        return surface

