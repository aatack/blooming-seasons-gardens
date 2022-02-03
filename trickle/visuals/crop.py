import pygame
from trickle.visuals.empty import Empty
from trickle.visuals.overlay import Overlay
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


class Crop(Visual):
    def __init__(self, visual: Visual, width: float, height: float):
        """Represents a repositioned visual."""
        self.visual = visual
        self.width = width
        self.height = height

    def simplify(self) -> "Visual":
        from trickle.visuals.reposition import Reposition

        simplified_visual = self.visual.simplify()

        if (
            isinstance(simplified_visual, Empty)
            or (self.right() <= self.left())
            or (self.bottom() <= self.top())
        ):
            return Empty()

        elif isinstance(simplified_visual, Overlay):
            return Overlay(
                *[
                    Crop(visual, self.width, self.height).simplify()
                    for visual in simplified_visual.visuals
                ]
            ).simplify()  # TODO: is this final simplify needed?

        elif isinstance(simplified_visual, Reposition):
            # TODO: work out if this can be reliably simplified further, but probably
            #       not
            return Crop(simplified_visual, self.width, self.height)

        elif isinstance(simplified_visual, Surface):
            return Surface(
                simplified_visual.surface.subsurface(
                    0, 0, int(self.width), int(self.height)
                ),
                x=simplified_visual.x,
                y=simplified_visual.y,
            )

        elif isinstance(simplified_visual, Crop):
            return Crop(
                simplified_visual.visual,
                min(self.width, simplified_visual.width),
                min(self.height, simplified_visual.height),
            )

        else:
            raise Exception("Implementation error")

    def render(self, surface: pygame.Surface):
        visual_surface = pygame.Surface((int(self.width), int(self.height)))
        self.visual.render(visual_surface)
        # TODO: consider adding a starting x and y
        surface.blit(visual_surface, (0, 0))

    def top(self) -> float:
        return max(0.0, self.visual.top())

    def left(self) -> float:
        return max(0.0, self.visual.left())

    def bottom(self) -> float:
        return min(self.height, self.visual.bottom())

    def right(self) -> float:
        return min(self.width, self.visual.right())
