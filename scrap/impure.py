from scrap.base import Scrap, defscrap
from scrap.data import Literal, Message
from typing import Optional
import time


@defscrap
class Timer:
    start_time: Optional[float] = None

    def Start(self) -> Scrap:
        return Timer(time.time())

    def Read(self) -> Scrap:
        return Message(self, Literal(time.time() - self.start_time))
