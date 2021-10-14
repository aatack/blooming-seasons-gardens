from typing import Any, Callable, Optional, NamedTuple, Set
import abc


class Event(NamedTuple):
    source: Optional["State"] = None


class State(abc.ABC):
    def __init__(self):
        self._listeners: Set[State] = set()

    @abc.abstractmethod
    def value(self) -> Any:
        """Return the current value of the state."""

    @abc.abstractmethod
    def respond(self, event: Event):
        """Respond to an event caused by a state to which this state is listening."""

    def listen(self, state: "State"):
        """Denote that this state should receive broadcasts from another one."""
        # TODO: check for cyclic dependencies
        assert (
            self not in state._listeners
        ), "The given state is already listening for this one"
        state._listeners.add(self)

    def ignore(self, state: "State"):
        """Stop listening for events caused by the given state."""
        assert self in state._listen, "The given state is not being listened for"
        state._listeners.remove(self)

    def broadcast(self, event: Event):
        """Called whenever an event happens which changes the state's value."""
        assert event.source is self, "States can only broadcast events about themselves"
        for state in self._listeners:
            state.respond(event)

    def log(self) -> "State":
        _ = _Log(self)
        return self


class Changed(Event, NamedTuple):
    old: Optional[Any]
    new: Optional[Any]
    source: Optional["Event"] = None


class Variable(State):
    def __init__(self, value: Optional[Any] = None):
        super().__init__()
        self._value = value

    def value(self) -> Optional[Any]:
        return self._value

    def respond(self, event: Event):
        pass

    def modify(self, new: Optional[Any]):
        event = Changed(self._value, new, self)
        self._value = new
        if event.old != event.new:
            self.broadcast(event)


class Derived(State):
    def __init__(self, function: Callable, *args: State, **kwargs: State):
        super().__init__()

        self._function = function
        self._args = args
        self._kwargs = kwargs

        self._value = self._compute()

        for arg in self._args:
            self.listen(arg)
        for kwarg in self._kwargs.values():
            self.listen(kwarg)

    def value(self) -> Optional[Any]:
        return self._value

    def _compute(self) -> Optional[Any]:
        return self._function(
            *[state.value() for state in self._args],
            **{key: state.value() for key, state in self._kwargs.items()}
        )

    def respond(self, event: Event):
        event = Changed(self._value, self._compute(), self)
        self._value = event.new
        if event.old != event.new:
            self.broadcast(event)


class _Log(State):
    def __init__(self, state: State, message: str = "State changed:"):
        super().__init__()
        self._state = state
        self._message = message

        self.listen(self._state)

    def value(self):
        return self._state

    def respond(self, _: Event):
        print(self._message, self._state.value())
