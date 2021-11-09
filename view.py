import pygame
from typing import Tuple, Union, List


View = Union[pygame.Surface, Tuple[float, float, "View"], List["View"]]


def simplify(view: View) -> List[Tuple[float, float, View]]:
    """Simplify any nested hierarchy of views into a list of translated literals."""
    if isinstance(view, pygame.Surface):
        return [(0.0, 0.0, view)]
    elif isinstance(view, tuple):
        outer_x, outer_y, inner_view = view
        return [
            (outer_x + inner_x, outer_y + inner_y, surface)
            for inner_x, inner_y, surface in simplify(inner_view)
        ]
    elif isinstance(view, list):
        result = []
        for inner_view in view:
            result.extend(simplify(inner_view))
        return result
    else:
        raise ValueError(f"Unexpected view: {view} of type {type(view)}")
