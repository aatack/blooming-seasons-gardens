from typing import NamedTuple, Tuple, Optional, Union
from math import pi, cos, sin


class Point(NamedTuple):
    x: float
    y: float

    def translate(self, right: float = 0.0, down: float = 0.0) -> "Point":
        return Point(self.x + right, self.y + down)

    def rotate(self, turns_anticlockwise: float) -> "Point":
        # TODO: efficient cases for common turns (ie. half turn, quarter turn)
        radians = turns_anticlockwise * 2 * pi
        cosine = cos(radians)
        sine = sin(radians)
        return Point(
            (self.x * cosine) - (self.y * sine), (self.y * cosine) + (self.x * sine)
        )

    def scale(self, factor: float) -> "Point":
        return Point(self.x * factor, self.y * factor)

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"


class UnderSpecified(Exception):
    """Denotes that a bounding box is underspecified."""


class OverSpecified(Exception):
    """Denotes that a bounding box is overspecified."""


class IncorrectImplementation(Exception):
    """Denotes that there has been an error in the implementation."""


class LatentBoundingBox(NamedTuple):
    """Stores minimal information about the position and size of a bounding box."""

    left: float
    right: float
    top: float
    bottom: float


class _DimensionBounds(NamedTuple):
    lower: Optional[float]
    upper: Optional[float]
    centre: Optional[float]
    size: Optional[float]

    def compute_bounds(self) -> Tuple[float, float]:
        # TODO: informative error messages
        lower, upper, centre, size = self.lower, self.upper, self.centre, self.size
        specified_values = [
            value for value in (lower, upper, centre, size) if value is not None
        ]
        if len(specified_values) < 2:
            raise UnderSpecified()
        if len(specified_values) > 2:
            raise OverSpecified()

        if lower is not None:
            if upper is not None:
                assert upper >= lower
                return lower, upper
            if centre is not None:
                assert centre >= lower
                return lower, lower + (2 * (centre - lower))
            if size is not None:
                assert size >= 0
                return lower, lower + size
        if upper is not None:
            if centre is not None:
                assert centre <= upper
                return upper - (2 * (upper - centre)), upper
            if size is not None:
                assert size >= 0
                return upper - size, upper
        if centre is not None:
            if size is not None:
                assert size >= 0
                half_size = size * 0.5
                return centre - half_size, centre + half_size

        raise IncorrectImplementation()


class BoundingBox:
    """Provides a pleasant interface for describing an axis-aligned bounding box."""

    def __init__(
        self,
        latent: Optional[Union[LatentBoundingBox, "BoundingBox"]] = None,
        *,
        left: Optional[float] = None,
        right: Optional[float] = None,
        top: Optional[float] = None,
        bottom: Optional[float] = None,
        centre: Optional[Union[float, Tuple[Optional[float], Optional[float]]]] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ):
        # TODO: informative error messages
        if latent is not None:
            self._latent = (
                latent if isinstance(latent, LatentBoundingBox) else latent._latent
            )
            assert all(
                value is None
                for value in (left, right, top, bottom, centre, width, height)
            )
        else:
            if isinstance(centre, tuple):
                horizontal_centre, vertical_centre = centre
            else:
                horizontal_centre, vertical_centre = centre, centre

            horizontal_bounds = _DimensionBounds(left, right, horizontal_centre, width)
            vertical_bounds = _DimensionBounds(top, bottom, vertical_centre, height)

            self._latent = LatentBoundingBox(
                *horizontal_bounds.compute_bounds(), *vertical_bounds.compute_bounds()
            )

    def __str__(self) -> str:
        return (
            f"BoudningBox(left={self._latent.left}, right={self._latent.right}, "
            + f"top={self._latent.top}, bottom={self._latent.bottom})"
        )

    # TODO: properties
