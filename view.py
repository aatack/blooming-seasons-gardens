import abc
import pygame
from typing import Tuple


class View(abc.ABC):
    """
    Abstract representation of a view of a 2D user interface.
    
    Used to simplify nested representations, preventing translations with negative
    offsets from cutting off some of the view during their resolution.
    """

    @abc.abstractmethod
    def resolve(self) -> pygame.Surface:
        """Resolve the view into a pygame surface."""

    @abc.abstractmethod
    def size(self) -> Tuple[int, int]:
        """Return the size of the view in pixels."""


class Literal(View):
    def __init__(self, surface: pygame.Surface):
        self.surface = surface

    def resolve(self) -> pygame.Surface:
        return self.surface

    def size(self) -> Tuple[int, int]:
        return self.surface.get_size()


class Translate(View):
    def __init__(self, view: View, x: float, y: float):
        self.view = view
        self.x = x
        self.y = y

    def resolve(self) -> pygame.Surface:
        raise NotImplementedError()
