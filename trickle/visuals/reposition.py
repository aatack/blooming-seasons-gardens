from typing import Callable, Optional

import pygame
from trickle.visuals.overlay import Overlay
from trickle.visuals.visual import Visual


class Reposition(Visual):
    def __init__(
        self,
        visual: Visual,
        *,
        horizontal_offset: float = 0.0,
        vertical_offset: float = 0.0,
        crop_left: Optional[float] = None,
        crop_top: Optional[float] = None,
        crop_right: Optional[float] = None,
        crop_bottom: Optional[float] = None,
    ):
        """
        Represents a repositioned visual.

        The child visual is first rendered, then cropped.  After cropping the remaining
        visual is moved according to the specified offsets.
        """
        self.visual = visual

        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset

        self.crop_left = crop_left
        self.crop_top = crop_top
        self.crop_right = crop_right
        self.crop_bottom = crop_bottom

    def simplify(self) -> "Visual":
        simplified_visual = self.visual.simplify()
        assert isinstance(simplified_visual, Overlay)

        visuals = []
        for visual in simplified_visual.visuals:
            assert isinstance(visual, Reposition)

            visuals.append(
                Reposition(
                    visual.visual,
                    horizontal_offset=self.horizontal_offset + visual.horizontal_offset,
                    vertical_offset=self.vertical_offset + visual.vertical_offset,
                    crop_left=_merge(
                        self.crop_left - visual.horizontal_offset
                        if self.crop_left is not None
                        else None,
                        visual.crop_left,
                        max,
                    ),
                    crop_top=_merge(
                        self.crop_top - visual.vertical_offset
                        if self.crop_top is not None
                        else None,
                        visual.crop_top,
                        max,
                    ),
                    crop_right=_merge(
                        self.crop_right - visual.horizontal_offset
                        if self.crop_right is not None
                        else None,
                        visual.crop_right,
                        min,
                    ),
                    crop_bottom=_merge(
                        self.crop_bottom - visual.vertical_offset
                        if self.crop_bottom is not None
                        else None,
                        visual.crop_bottom,
                        min,
                    ),
                )
            )

        return Overlay(*visuals)

    def render(self, surface: pygame.Surface):
        from trickle.visuals.surface import Surface

        # TODO: this could be accelerated by accounting for the different possible modes
        # TODO: these can be cached on construction if needed
        realised_visual_offset = (self.horizontal_offset, self.vertical_offset)
        realised_crop_offset = (
            0.0 if self.crop_left is None else self.crop_left,
            0.0 if self.crop_top is None else self.crop_top,
        )
        realised_crop_size = (
            max(
                0,
                self.visual.horizontal_extent() - realised_crop_offset[0]
                if self.crop_right is None
                else self.crop_right - realised_crop_offset[0],
            ),
            max(
                0,
                self.visual.vertical_extent() - realised_crop_offset[1]
                if self.crop_bottom is None
                else self.crop_bottom - realised_crop_offset[1],
            ),
        )
        actual_offset = tuple(
            map(sum, zip(realised_visual_offset, realised_crop_offset))
        )

        # NOTE: here we make some assumptions about how blit works with cropping.  It is
        #       assumed that the crop is applied before the offset, and that the cropped
        #       section of the image is not recentred.  So if the left were cropped by
        #       10 pixels, and the horizontal offset were 20, we expect there to be at
        #       least 30 empty pixels between the origin and the start of the visual
        #       along the relevant axis.  If this is not the case, a small wrapper
        #       around `surface.blit` may need to be implemented

        def to_ints(floats: tuple) -> tuple:
            return tuple(int(f) for f in floats)

        surface.blit(
            self.visual.render_from_scratch(transparent=True),
            to_ints(actual_offset),
            to_ints(realised_crop_offset + realised_crop_size),
        )

    def horizontal_extent(self) -> float:
        extent = self.visual.horizontal_extent()
        if self.crop_right is not None:
            extent = self.crop_right
        return extent + self.horizontal_offset

    def vertical_extent(self) -> float:
        extent = self.visual.vertical_extent()
        if self.crop_bottom is not None:
            extent = self.crop_bottom
        return extent + self.vertical_offset


def _merge(
    left: Optional[float],
    right: Optional[float],
    criterion: Callable[[float, float], float],
) -> Optional[float]:
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return criterion(left, right)
