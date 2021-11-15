import pygame
from typing import Tuple, Union, List, Optional


View = Union[pygame.Surface, Tuple[float, float, "View"], List["View"]]


def simplify(view: Optional[View]) -> List[Tuple[float, float, View]]:
    """Simplify any nested hierarchy of views into a list of translated literals."""
    if view is None:
        return []
    elif isinstance(view, pygame.Surface):
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


def render(view: Optional[View], surface: pygame.Surface, simplified: bool = False):
    if not simplified:
        view = simplify(view)

    assert isinstance(view, list)
    for x, y, inner_surface in view:
        surface.blit(inner_surface, (int(x), (int(y))))


def empty(width: int, height: int, transparent: bool = False) -> pygame.Surface:
    if transparent:
        return pygame.Surface((width, height), pygame.SRCALPHA)
    else:
        return pygame.Surface((width, height))


def height(view: List[Tuple[float, float, pygame.Surface]]) -> float:
    assert isinstance(view, list), "View must be in simplified form"
    return max([h + s.get_size()[1] for _, h, s in view])
