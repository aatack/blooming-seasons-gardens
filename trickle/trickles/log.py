from typing import Any, Callable, Optional, Union

from trickle.trickles.trickle import Path, Trickle


class Log(Trickle):
    """Trickle which prints all events coming through it."""

    def __init__(
        self,
        message: Optional[Union[str, Callable[[Trickle], str]]] = None,
        predicate: Optional[Callable] = None,
    ):
        super().__init__()

        self.message = message if message is not None else f"Log_{id(self)}"
        self.predicate = predicate

    def respond(self, path: Path, event: Any):
        if self.predicate is None or self.predicate(path, event):
            message = (
                self.message
                if isinstance(self.message, str)
                else self.message(self.input_map[path])
            )
            print(path, event, message)
