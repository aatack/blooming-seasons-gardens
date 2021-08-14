from scrap.base import Scrap
from scrap.data import Message
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
        messages = []

        for child in self.children:
            rebuilt_child = child.handle(event)
            if isinstance(rebuilt_child, Message):
                messages.append(rebuilt_child.message)
                rebuilt_child = rebuilt_child.scrap
            if rebuilt_child is not child:
                requires_rebuild = True
            rebuilt_children.append(rebuilt_child)

        handled_result = Group(*rebuilt_children) if requires_rebuild else self
        return (
            handled_result
            if len(messages) == 0
            else Message(handled_result, Group(*messages))
        )

    def __str__(self) -> str:
        return f"[{', '.join(str(child) for child in self.children)}]"
