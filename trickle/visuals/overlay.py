import pygame
from trickle.visuals.visual import Visual


class Overlay(Visual):
    def __init__(self, *visuals: Visual):
        self.visuals = visuals

    def _simplify(self) -> "Visual":
        visuals = []

        for visual in self.visuals:
            simplified_visual = visual.simplify()
            if isinstance(simplified_visual, Overlay):
                # TODO: work out how to handle multiple empty visuals
                visuals.extend(simplified_visual.visuals)
            else:
                visuals.append(simplified_visual)

        return Overlay(*visuals)

    def render(self, surface: pygame.Surface):
        for visual in self.visuals:
            visual.render(surface)

    def top(self) -> float:
        return min(visual.top() for visual in self.visuals)

    def left(self) -> float:
        return min(visual.left() for visual in self.visuals)

    def bottom(self) -> float:
        return max(visual.bottom() for visual in self.visuals)

    def right(self) -> float:
        return max(visual.right() for visual in self.visuals)
