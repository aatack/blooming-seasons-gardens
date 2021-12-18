from typing import Optional

import pygame
from trickle.visuals.overlay import Overlay
from trickle.visuals.visual import Visual


class Reposition(Visual):
    def __init__(
        self,
        visual: Visual,
        horizontal_offset: float = 0.0,
        vertical_offset: float = 0.0,
        horizontal_crop: Optional[float] = None,
        vertical_crop: Optional[float] = None,
    ):
        self.visual = visual

        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset

        self.horizontal_crop = horizontal_crop
        self.vertical_crop = vertical_crop

    def simplify(self) -> "Visual":
        simplified_visual = self.visual.simplify()
        assert isinstance(simplified_visual, Overlay)

        visuals = []
        for visual in simplified_visual.visuals:
            assert isinstance(visual, Reposition)
            visuals.append(
                Reposition(
                    visual.visual,
                    self.horizontal_offset + visual.horizontal_offset,
                    self.vertical_offset + visual.vertical_offset,
                    _compound_crops(self.horizontal_crop, visual.horizontal_crop),
                    _compound_crops(self.vertical_crop, visual.vertical_crop),
                )
            )

        return Overlay(*visuals)

    def render(self, surface: pygame.Surface):
        from trickle.visuals.surface import Surface

        # TODO: this could be accelerated by checking whether `self.visual` is an
        #       instance of `Surface(Visual)`.  If it is, we can skip the additional
        #       rendering step and just use its inner surface directly

        base_surface = Surface.empty(
            self.visual.horizontal_extent()
            if self.horizontal_crop is None
            else self.horizontal_crop,
            self.visual.vertical_extent()
            if self.vertical_crop is None
            else self.vertical_crop,
            transparent=True,
        )
        self.visual.render(base_surface)

        surface.blit(base_surface, (self.horizontal_offset, self.vertical_offset))

    def horizontal_extent(self) -> float:
        return self.horizontal_offset + (
            self.horizontal_crop
            if self.horizontal_crop is not None
            else self.visual.horizontal_extent()
        )

    def vertical_extent(self) -> float:
        return self.vertical_offset + (
            self.vertical_crop
            if self.vertical_crop is not None
            else self.visual.vertical_extent()
        )


def _compound_crops(left: Optional[float], right: Optional[float]) -> Optional[float]:
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return min(left, right)
