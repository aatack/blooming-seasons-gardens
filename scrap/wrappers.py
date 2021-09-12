from scrap.base import defscrap, Scrap, rebuild
from scrap.composite import Wrapper
from scrap.data import Message, Point
from scrap.control import UpdateWrapper
from scrap.impure import Timer
from scrap.event import Button, Click
from typing import Optional


@defscrap
class CatchClicks(Wrapper):
    button: int = 1
    minimum_time: Optional[int] = None
    timer: Optional[Timer] = None
    location: Optional[Point] = None

    def Button(self, button: int, x: float, y: float, down: bool, event: ...) -> Scrap:
        # TODO: clean this up
        fallback = self._DEFINITION.handlers.fallback
        if button != self.button:
            return fallback(self, event)

        contains = self.Contains(x, y).message.value

        if down:
            if contains:
                if self.minimum_time is None:
                    return UpdateWrapper(
                        self.wrap.Click(self.button, x, y),
                        dict(timer=None, location=None),
                    )
                else:
                    return UpdateWrapper(
                        self.wrap, dict(timer=Timer().Start(), location=Point(x, y))
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
                    self.wrap.Click(self.button, self.location.x, self.location.y),
                    dict(timer=None, location=None),
                )
            return UpdateWrapper(self.wrap, dict(timer=None, location=None))
