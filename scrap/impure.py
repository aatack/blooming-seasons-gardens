from scrap.base import Scrap
import time


class Timer(Scrap):
    class Start(Scrap):
        """Starts a timer."""

    @staticmethod
    def new() -> "Timer":
        return Timer().handle(Timer.Start())

    def __init__(self):
        self.start_time: Optional[float] = None

    def handle(self, event: Scrap) -> Scrap:
        if isinstance(event, Timer.Start):
            self.start_time = time.time()

        return self

    @property
    def started(self) -> bool:
        return self.start_time is not None

    @property
    def time(self) -> float:
        assert self.started, "Timer has not yet been started"
        return time.time() - self.start_time
