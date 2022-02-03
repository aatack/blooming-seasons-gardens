import pygame
from trickle.visuals.visual import Visual


class Overlay(Visual):
    def __init__(self, *visuals: Visual):
        self.visuals = visuals

    def simplify(self) -> "Visual":
        visuals = []

        for visual in self.visuals:
            simplified_visual = visual.simplify()
            if isinstance(simplified_visual, Overlay):
                visuals.extend(simplified_visual.visuals)
            else:
                visuals.extend(simplified_visual)

        return Overlay(*visuals)

    def render(self, surface: pygame.Surface):
        for visual in self.visuals:
            visual.render(surface)

    def top(self) -> float:
        return min(visual.top() for visual in self.visuals)

    def left(self) -> float:
        return min(visual.bottom() for visual in self.visuals)

    def bottom(self) -> float:
        return max(visual.bottom() for visual in self.visuals)

    def right(self) -> float:
        return max(visual.right() for visual in self.visuals)
