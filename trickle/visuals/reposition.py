from typing import Optional

import pygame
from trickle.visuals.overlay import Overlay
from trickle.visuals.visual import Visual


class Reposition(Visual):
    def __init__(
        self,
        visual: Visual,
        *,
        crop_bottom: Optional[float] = None,
        crop_right: Optional[float] = None,
        crop_top: float = 0.0,
        crop_left: float = 0.0,
        horizontal_offset: float = 0.0,
        vertical_offset: float = 0.0,
    ):
        """
        Represents a repositioned visual.

        The child visual is first rendered, then cropped.  After cropping the remaining
        visual is moved according to the specified offsets.
        """
        self.visual = visual

        self.crop_bottom = crop_bottom
        self.crop_right = crop_right
        self.crop_top = crop_top
        self.crop_left = crop_left

        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset

        assert self.crop_top >= 0.0
        assert self.crop_left >= 0.0

        # Under certain circumstances the crops will overlap, which will result in no
        # visual being rendered at all
        self.empty = (
            (self.crop_bottom is not None) and self.crop_bottom <= self.crop_top
        ) or ((self.crop_right is not None) and self.crop_right <= self.crop_left)

    def simplify(self) -> "Visual":
        simplified_visual = self.visual.simplify()
        assert isinstance(simplified_visual, Overlay)

        visuals = []
        for visual in simplified_visual.visuals:
            assert isinstance(visual, Reposition)

            raise NotImplementedError()

        return Overlay(*visuals)

    def render(self, surface: pygame.Surface):
        from trickle.visuals.surface import Surface

        # TODO: this could be accelerated by checking whether `self.visual` is an
        #       instance of `Surface(Visual)`.  If it is, we can skip the additional
        #       rendering step and just use its inner surface directly

        base_surface = Surface.empty(
            self.visual.horizontal_extent()
            if self.crop_right is None
            else self.crop_right,
            self.visual.vertical_extent()
            if self.crop_bottom is None
            else self.crop_bottom,
            transparent=True,
        )
        self.visual.render(base_surface)

        crop_position = (int(self.crop_left), int(self.crop_top))
        crop_size = tuple(
            base - crop for base, crop in zip(base_surface.get_size(), crop_position)
        )

        surface.blit(
            base_surface,
            (int(self.horizontal_offset), int(self.vertical_offset)),
            crop_position + crop_size,
        )

    def horizontal_extent(self) -> float:
        extent = self.visual.horizontal_extent()
        if self.crop_right is not None:
            extent = min(extent, self.crop_right)
        extent -= self.crop_left
        return extent + self.horizontal_offset

    def vertical_extent(self) -> float:
        extent = self.visual.vertical_extent()
        if self.crop_bottom is not None:
            extent = min(extent, self.crop_bottom)
        extent -= self.crop_top
        return extent + self.vertical_offset


def _compound_crops(left: Optional[float], right: Optional[float]) -> Optional[float]:
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return min(left, right)
