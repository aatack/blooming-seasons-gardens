from scrap.base import defscrap, Scrap
from scrap.data import Point, Literal
from scrap.composite import Group
from typing import List


@defscrap
class Contains:
    point: Point

    def Group(self, children: List[Scrap]) -> Scrap:
        for child in children:
            if isinstance(child, Literal) and (child.value is True):
                return Literal(True)
        return Literal(False)

    def _fallback(self, event: Scrap) -> Scrap:
        # Override default behaviour of returning self
        return event
