from typing import Any, Optional, NamedTuple, Set
import abc


class Event(NamedTuple):
    source: Optional["State"] = None


class State(abc.ABC):
    def __init__(self):
        self._listeners: Set[State] = set()

    @abc.abstractmethod
    def state(self) -> Any:
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
