import pygame
from trickle.visuals.visual import Visual


class Overlay(Visual):
    def __init__(self, *visuals: Visual):
        self.visuals = visuals

    def simplify(self) -> "Visual":
        visuals = []

        for visual in self.visuals:
            simplified_visual = visual.simplify()
            assert isinstance(simplified_visual, Overlay)
            visuals.extend(simplified_visual.visuals)

        return Overlay(*visuals)

    def render(self, surface: pygame.Surface):
        for visual in self.visuals:
            visual.render(surface)

    def horizontal_extent(self) -> float:
        return max(visual.horizontal_extent() for visual in self.visuals)

    def vertical_extent(self) -> float:
        return max(visual.vertical_extent() for visual in self.visuals)
