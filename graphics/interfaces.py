import abc
import pygame

from graphics.bounding_box import BoundingBox


class Renderable(abc.ABC):
    @abc.abstractmethod
    def render(self, surface: pygame.Surface):
        """Render an object onto the given surface."""

    @abc.abstractmethod
    def bounds(self) -> BoundingBox:
        """Return a bounding box bounding the rendered part of the object."""


class Translatable(abc.ABC):
    @abc.abstractmethod
    def translate(self, right: float = 0, down: float = 0) -> "Translatable":
        """Return a representation of the object after it has been translated."""


class Rotatable(abc.ABC):
    @abc.abstractmethod
    def rotate(self, turns_anticlockwise: float) -> "Rotatable":
        """Rotate the object anticlockwise by the specified number of turns."""


class Scalable(abc.ABC):
    @abc.abstractmethod
    def scale(self, factor: float) -> "Scalable":
        """Scale the object by a given factor about the origin."""
