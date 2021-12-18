import pygame
from trickle.visuals.overlay import Overlay
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


class Peek(Visual):
    def __init__(self, visual: Visual, width: float, height: float):
        self.visual = visual
        self.width = width
        self.height = height

    def simplify(self) -> "Visual":
        simplified_visual = self.visual.simplify()

        if isinstance(simplified_visual, Overlay):
            return Peek(
                simplified_visual.horizontal_extent(),
                simplified_visual.vertical_extent(),
                simplified_visual,
            )
        elif isinstance(simplified_visual, Peek):
            return Peek(
                min(self.width, simplified_visual.width),
                min(self.height, simplified_visual.height),
                simplified_visual.visual,
            )
        else:
            raise Visual.invalid_simplified(simplified_visual)

    def render(self, surface: pygame.Surface):
        peek = Surface.empty(self.width, self.height, transparent=True).surface
        self.visual.render(peek)

        # TODO: in theory we could simplify compositions of positions and peeks by
        #       setting the position here, thereby requiring fewer blits
        surface.blit(peek, (0, 0))

    def horizontal_extent(self) -> float:
        return self.width

    def vertical_extent(self) -> float:
        return self.height
