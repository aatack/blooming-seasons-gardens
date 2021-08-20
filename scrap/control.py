from scrap.base import defscrap, Scrap
from typing import Dict, Any


@defscrap
class UpdateWrapper:
    result: Scrap
    updates: Dict[str, Any]


@defscrap
class Translate:
    vector: Point


@defscrap
class Scale:
    scale: float
