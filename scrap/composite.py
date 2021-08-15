from scrap.base import defscrap, Scrap
from scrap.data import Message, Literal
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
            rebuilt_child = child._handle(event)
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
            return Message(result.scrap, event._handle(result.message))
        return result

    def _cache(self) -> renderable.Renderable:
        return renderable.Group([child._cache() for child in self.children])


class CatchClicks(Scrap):
    def __init__(
        self,
        scrap: Scrap,
        minimum_time: Optional[int] = None,
        button: int = 1,
        timer: Optional[Timer] = None,
    ):
        self.scrap = scrap
        self.minimum_time = minimum_time
        self.button = button
        self.timer = timer

    def cache(self) -> renderable.Renderable:
        """Return a cached version of the rendered view of this scrap."""
        return self.scrap.cache()

    def render(self, surface: pygame.Surface):
        """Render the scrap to a pygame surface."""
        self.scrap.render(surface)

    def handle(self, event: Scrap) -> Scrap:
        timer = self.timer

        if isinstance(event, Button) and event.button == self.button:
            contains = self.scrap.handle(Contains(event.location))
            assert isinstance(contains, Message)
            hit = (
                True
                if (
                    isinstance(contains.message, Literal)
                    and (contains.message.value is True)
                )
                else False
            )

            if event.down and hit:
                if self.minimum_time is None:
                    scrap = self.scrap.handle(Click(self.button, event.location))
                else:
                    return CatchClicks(
                        self.scrap,
                        minimum_time=self.minimum_time,
                        button=self.button,
                        timer=Timer.new(),
                    )
            elif event.up and hit:
                if self.timer is None or self.timer.time < self.minimum_time:
                    return self
                else:
                    scrap = self.scrap.handle(Click(self.button, event.location))
            else:
                return CatchClicks(
                    self.scrap, minimum_time=self.minimum_time, button=self.button,
                )
        else:
            scrap = self.scrap.handle(event)

        if scrap is self.scrap:
            return self

        if isinstance(scrap, Message):
            return Message(
                CatchClicks(
                    scrap.scrap,
                    minimum_time=self.minimum_time,
                    button=self.button,
                    timer=self.timer,
                )
                if scrap.scrap is not self.scrap
                else self,
                scrap.message,
            )
        else:
            return (
                CatchClicks(
                    scrap,
                    minimum_time=self.minimum_time,
                    button=self.button,
                    timer=timer,
                )
                if scrap is not self.scrap
                else self
            )
