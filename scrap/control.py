from scrap.base import defscrap, Scrap
from scrap.data import Vector
from typing import Dict, Any, Optional


@defscrap
class UpdateWrapper:
    result: Scrap
    updates: Dict[str, Any]


@defscrap
class Scale:
    scale: float


@defscrap
class Translate(Vector):
    pass


@defscrap
class Resize:
    width: Optional[float] = None
    height: Optional[float] = None


@defscrap
class ResizeWindow(Resize):
    """A resize event that specifically comes from the outermost window."""
