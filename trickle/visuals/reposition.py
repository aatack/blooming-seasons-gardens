import pygame
from trickle.visuals.empty import Empty
from trickle.visuals.overlay import Overlay
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


class Reposition(Visual):
    def __init__(self, visual: Visual, x: float = 0.0, y: float = 0.0):
        """Represents a repositioned visual."""
        self.visual = visual
        self.x = x
        self.y = y

    def simplify(self) -> "Visual":
        from trickle.visuals.crop import Crop

        simplified_visual = self.visual.simplify()

        if isinstance(simplified_visual, Empty):
            return Empty(self)

        elif isinstance(simplified_visual, Overlay):
            return Overlay(
                *[
                    Reposition(visual, x=self.x, y=self.y).simplify()
                    for visual in simplified_visual.visuals
                ]
            ).simplify()  # TODO: is this final simplify needed?

        elif isinstance(simplified_visual, Reposition):
            return Reposition(
                simplified_visual.visual,
                x=self.x + simplified_visual.x,
                y=self.y + simplified_visual.y,
            ).simplify()

        elif isinstance(simplified_visual, Surface):
            return Surface(
                simplified_visual.surface,
                x=self.x + simplified_visual.x,
                y=self.y + simplified_visual.y,
            )

        elif isinstance(simplified_visual, Crop):
            # TODO: work out if this can be reliably simplified further, but probably
            #       not
            return Reposition(simplified_visual, x=self.x, y=self.y)

        else:
            raise Exception("Implementation error")

    def render(self, surface: pygame.Surface):
        surface.blit(
            self.visual.render_from_scratch(transparent=True),
            (int(self.x), int(self.y)),
        )

    def top(self) -> float:
        return self.visual.top() + self.y

    def left(self) -> float:
        return self.visual.left() + self.x

    def bottom(self) -> float:
        return self.visual.bottom() + self.y

    def right(self) -> float:
        return self.visual.right() + self.x
