import pygame
from typing import Tuple, Union, List, Optional, NamedTuple


View = Optional[Union[pygame.Surface, List["View"], "Position"]]


class Position(NamedTuple):
    x: float
    y: float
    view: View


def simplify(view: View) -> View:
    """Simplify any nested hierarchy of views into a list of translated literals."""
    if view is None:
        return []
    elif isinstance(view, pygame.Surface):
        return [Position(0.0, 0.0, view)]
    elif isinstance(view, list):
        result = []
        for inner_view in view:
            result.extend(simplify(inner_view))
        return result
    elif isinstance(view, Position):
        outer_x, outer_y, inner_view = view
        return [
            Position(outer_x + inner_x, outer_y + inner_y, surface)
            for inner_x, inner_y, surface in simplify(inner_view)
        ]
    else:
        raise ValueError(f"Unexpected view: {view} of type {type(view)}")


def render(view: View, surface: pygame.Surface):
    """
    Render the view to a surface.
    
    May not work properly if the view has not first been simplified.
    """
    if view is None:
        return
    elif isinstance(view, pygame.Surface):
        surface.blit(view, (0, 0))
    elif isinstance(view, list):
        for view_element in view:
            render(view_element, surface)
    elif isinstance(view, Position):
        x, y, inner_surface = view
        assert isinstance(inner_surface, pygame.Surface)
        surface.blit(inner_surface, (int(x), (int(y))))
    else:
        raise ValueError(f"Unexpected view: {view} of type {type(view)}")


def empty(width: int, height: int, transparent: bool = False) -> pygame.Surface:
    if transparent:
        return pygame.Surface((width, height), pygame.SRCALPHA)
    else:
        return pygame.Surface((width, height))


def height(view: List[Tuple[float, float, pygame.Surface]]) -> float:
    if view is None:
        return 0
    elif isinstance(view, pygame.Surface):
        return view.get_size()[1]
    elif isinstance(view, list):
        return max([height(view_element) for view_element in view])
    elif isinstance(view, Position):
        return view.y + height(view.view)
    else:
        raise ValueError(f"Unexpected view: {view} of type {type(view)}")


def width(view: List[Tuple[float, float, pygame.Surface]]) -> float:
    if view is None:
        return 0
    elif isinstance(view, pygame.Surface):
        return view.get_size()[0]
    elif isinstance(view, list):
        return max([width(view_element) for view_element in view])
    elif isinstance(view, Position):
        return view.x + width(view.view)
    else:
        raise ValueError(f"Unexpected view: {view} of type {type(view)}")
