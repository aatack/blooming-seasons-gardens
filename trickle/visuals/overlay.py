import pygame
from trickle.visuals.visual import Visual


class Overlay(Visual):
    def __init__(self, *visuals: Visual):
        self.visuals = visuals

    def simplify(self) -> "Visual":
        visuals = []

        for visual in self.visuals:
            simplified_visual = visual.simplify()
            # TODO: handle peeks
            if isinstance(simplified_visual, Overlay):
                visuals.extend(simplified_visual.visuals)
            else:
                raise Visual.invalid_simplified(simplified_visual)

        return Overlay(*visuals)

    def render(self, surface: pygame.Surface):
        for visual in self.visuals:
            visual.render(surface)

    def width(self) -> float:
        return max(visual.width() for visual in self.visuals)

    def height(self) -> float:
        return max(visual.height() for visual in self.visuals)
