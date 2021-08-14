from scrap.base import defscrap, Scrap
from scrap.data import Message, Literal
from scrap.queries import Contains
from scrap.impure import Timer
from scrap.event import Button, Click
import wrapper.renderable as renderable
import pygame
from typing import List, Optional


@defscrap
class Void:
    """Scrap for which any handling scrap will return itself."""


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
