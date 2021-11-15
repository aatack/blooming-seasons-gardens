import pygame
from typing import Tuple, Union, List, Optional, NamedTuple


View = Optional[Union[pygame.Surface, List["View"], "Position"]]


class Position(NamedTuple):
    x: float
    y: float
    view: View


class Peek(NamedTuple):
    width: float
    height: float
    view: View


def simplify(view: View) -> Union[list, "Peek"]:
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
        simplified = simplify(view.view)
        if isinstance(simplified, list):
            return [
                Position(
                    view.x + simplified_child.x,
                    view.y + simplified_child.y,
                    simplified_child.view,
                )
                for simplified_child in simplified
            ]
        elif isinstance(simplified, Peek):
            return [Position(view.x, view.y, simplified)]
    elif isinstance(view, Peek):
        return Peek(view.width, view.height, simplify(view.view))
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
        x, y, child = view
        if isinstance(child, pygame.Surface):
            surface.blit(child, (int(x), (int(y))))
        elif isinstance(child, Peek):
            peek = empty(int(child.width), int(child.height), transparent=True)
            render(child.view, peek)
            surface.blit(peek, (0, 0))
        else:
            raise ValueError(
                f"Unexpected position child: {child} of type {type(child)}"
            )
    elif isinstance(view, Peek):
        peek = empty(int(view.width), int(view.height), transparent=True)
        render(view.view, peek)
        surface.blit(peek, (0, 0))
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
    elif isinstance(view, Peek):
        return view.height
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
    elif isinstance(view, Peek):
        return view.width
    else:
        raise ValueError(f"Unexpected view: {view} of type {type(view)}")
