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
        
        The simplified visual must either be a Peek, or an Overlay containing only
        Reposition visuals.
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

    @staticmethod
    def is_valid_simplified(visual: "Visual") -> bool:
        from trickle.visuals.overlay import Overlay
        from trickle.visuals.peek import Peek
        from trickle.visuals.reposition import Reposition

        if isinstance(visual, Overlay):
            return all(
                isinstance(child, Reposition)
                # TODO: also check that we do not have stacked reposition visuals
                and Visual.is_valid_simplified(child.visual)
                for child in visual.visuals
            )

        if isinstance(visual, Peek):
            return True

        return False

    @staticmethod
    def invalid_simplified(visual: "Visual") -> Exception:
        """Return an error denoting that a simplified visual is invalid."""
        return ValueError(f"Invalid simplified visual: {visual}")
