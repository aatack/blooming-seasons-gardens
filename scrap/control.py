from scrap.base import defscrap, Scrap
from scrap.data import Vector
from typing import Dict, Any


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
