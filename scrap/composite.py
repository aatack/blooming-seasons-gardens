from scrap.base import defscrap, Scrap, rebuild
from scrap.data import Message, Literal
from scrap.control import UpdateWrapper
import wrapper.renderable as renderable
import pygame
from typing import List


@defscrap
class Void:
    """Scrap for which any handling scrap will return itself."""

    def Render(self, render: ...) -> Scrap:
        return render


@defscrap
class Group:
    children: List[Scrap]

    def _fallback(self, event: Scrap) -> Scrap:
        requires_rebuild = False
        rebuilt_children = []
        messages = []

        for child in self.children:
            rebuilt_child = child[event]
            if isinstance(rebuilt_child, Message):
                messages.append(rebuilt_child.message)
                rebuilt_child = rebuilt_child.scrap
            if rebuilt_child is not child:
                requires_rebuild = True
            rebuilt_children.append(rebuilt_child)

        handled_result = Group(rebuilt_children) if requires_rebuild else self

        return (
            handled_result
            if len(messages) == 0
            else Message(handled_result, Group(messages))
        )

    def _postprocessor(self, result: Scrap, event: Scrap) -> Scrap:
        if isinstance(result, Message):
            return Message(result.scrap, event[result.message])
        return result

    def Render(self, render: ...) -> Scrap:
        for child in self.children:
            render = child[render]
        return render


@defscrap
class Wrapper:
    wrap: Scrap

    def _fallback(self, event: Scrap) -> Scrap:
        return self.wrap[event]

    def _postprocessor(self, result: Scrap, event: Scrap) -> Scrap:
        # TODO: clean this up
        wrapper_updates = {}
        if isinstance(result, UpdateWrapper):
            wrapper_updates = result.updates
            result = result.result

        scrap = result
        message = None
        if isinstance(result, Message):
            scrap = result.scrap
            message = result.message

        wrapped = (
            self
            if (scrap is self.wrap and len(wrapper_updates) == 0)
            else rebuild(self, wrap=scrap, **wrapper_updates)
        )
        return wrapped if message is None else Message(wrapped, message)

    def Cache(self) -> Scrap:
        return self.wrap.Cache()
