from scrap.base import Scrap
import wrapper.renderable as renderable
from typing import List


class Void(Scrap):
    """Scrap for which any handling scrap must return itself."""


class Group(Scrap):
    def __init__(self, *children: List[Scrap]):
        self.children = children

    def cache(self) -> renderable.Renderable:
        return renderable.Group(self.children)

    def handle(self, event: Scrap) -> Scrap:
        if isinstance(event, Void):
            return self

        requires_rebuild = False
        rebuilt_children = []

        for child in self.children:
            rebuilt_child = child.handle(event)
            if rebuilt_child is not child:
                requires_rebuild = True
            rebuilt_children.append(rebuilt_child)

        return Group(*rebuilt_children) if requires_rebuild else self
