from scrap.base import defscrap, Scrap, rebuild
from scrap.data import Message, Literal, Point
from scrap.control import UpdateWrapper
from scrap.impure import Timer
from scrap.event import Button, Click
import wrapper.renderable as renderable
import pygame
from typing import List, Optional


@defscrap
class Void:
    """Scrap for which any handling scrap will return itself."""


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

    def _cache(self) -> renderable.Renderable:
        return renderable.Group([child() for child in self.children])


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

    def _cache(self) -> renderable.Renderable:
        return self.wrap()


@defscrap
class CatchClicks(Wrapper):
    button: int = 1
    minimum_time: Optional[int] = None
    timer: Optional[Timer] = None
    location: Optional[Point] = None

    def Button(self, button: int, location: Point, down: bool, event: ...) -> Scrap:
        # TODO: clean this up
        fallback = self._DEFINITION.handlers.fallback
        if button != self.button:
            return fallback(self, event)

        contains = self.Contains(location).message.value

        if down:
            if contains:
                if self.minimum_time is None:
                    return UpdateWrapper(
                        self.wrap.Click(self.button, location),
                        dict(timer=None, location=None),
                    )
                else:
                    return UpdateWrapper(
                        self.wrap, dict(timer=Timer().Start(), location=location)
                    )
            else:
                return UpdateWrapper(self.wrap, dict(timer=None, location=None))

        else:
            # TODO: allow button presses to fall through under certain circumstances?
            if (
                contains
                and (self.timer is not None)
                and (self.timer.Read().message.value >= self.minimum_time)
            ):
                return UpdateWrapper(
                    self.wrap.Click(self.button, self.location),
                    dict(timer=None, location=None),
                )
            return UpdateWrapper(self.wrap, dict(timer=None, location=None))
