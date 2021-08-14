from scrap.base import Scrap
from scrap.data import Message, Literal
from scrap.queries import Contains
import wrapper.renderable as renderable
from typing import List, Optional


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

        reduced_message = self.reduce_messages(event, messages)

        return (
            handled_result
            if len(messages) == 0
            else Message(
                handled_result,
                Group(*messages) if reduced_message is None else reduced_message,
            )
        )

    def reduce_messages(self, event: Scrap, messages: List[Scrap]) -> Optional[Scrap]:
        """Reduce a list of messages if needed; if not, return None."""
        if isinstance(event, Contains):
            for message in messages:
                if isinstance(message, Literal) and message.value is True:
                    return Literal(True)
            return Literal(False)

        return None

    def __str__(self) -> str:
        return f"[{', '.join(str(child) for child in self.children)}]"
