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
        assert self in state._listeners, "The given state is not being listened for"
        state._listeners.remove(self)

    def broadcast(self, event: Event):
        """Called whenever an event happens which changes the state's value."""
        assert event.source is self, "States can only broadcast events about themselves"
        for state in self._listeners:
            state.respond(event)

    def log(self) -> "State":
        _ = _Log(self)
        return self


class Modified(Event, NamedTuple):
    old: Optional[Any]
    new: Optional[Any]
    source: Optional[State] = None


class Index(Event, NamedTuple):
    index: int
    event: Event
    source: Optional[State] = None


class Key(Event, NamedTuple):
    key: str
    event: Event
    source: Optional[State] = None


class Added(Event, NamedTuple):
    value: Optional[Any]
    source: Optional[State] = None


class Removed(Event, NamedTuple):
    index: int
    value: Optional[Any]
    source: Optional[State] = None


class Variable(State):
    def __init__(self, value: Optional[Any] = None):
        super().__init__()
        self._value = value

    def value(self) -> Optional[Any]:
        return self._value

    def respond(self, event: Event):
        pass

    def modify(self, new: Optional[Any]):
        event = Modified(self._value, new, self)
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
        event = Modified(self._value, self._compute(), self)
        self._value = event.new
        if event.old != event.new:
            self.broadcast(event)


class Ordered(State):
    def __init__(self, *elements: State):
        super().__init__()

        self._elements = list(elements)
        self._index = {element: i for i, element in enumerate(self._elements)}

        for element in self._elements:
            self.listen(element)

    def value(self):
        return [element.value() for element in self._elements]

    def respond(self, event: Event):
        self.broadcast(Index(self._index[event.source], event, self))

    def add(self, state: State):
        self._elements.append(state)
        self._index[state] = len(self._elements) - 1
        self.listen(state)
        self.broadcast(Added(state.value(), self))

    def remove(self, index: int):
        state = self._elements[index]
        self.ignore(state)
        self._elements = [
            element for i, element in enumerate(self._elements) if i != index
        ]
        self._index = {
            element: (i if i < index else i - 1) for element, i in self._index.items()
        }
        self.broadcast(Removed(index, state.value(), self))

    def __getitem__(self, index: int) -> State:
        return self._elements[index]


class Keyed(State):
    def __init__(self, **elements: State):
        super().__init__()

        self._elements = elements
        self._key = {element: key for key, element in self._elements.items()}

        for element in self._elements.values():
            self.listen(element)

    def value(self):
        return {key: element.value() for key, element in self._elements.items()}

    def respond(self, event: Event):
        self.broadcast(Key(self._key[event.source], event, self))

    # def add(self, key: str, state: State):
    #     assert key not in self._elements
    #     self._elements[key] = state
    #     self._key[state] = key
    #     self.listen(state)
    #     self.broadcast(Added(state.value(), self))

    def __getitem__(self, key: str) -> State:
        return self._elements[key]


class _Log(State):
    def __init__(self, state: State, message: str = "State updated:"):
        super().__init__()
        self._state = state
        self._message = message

        self.listen(self._state)

    def value(self):
        return self._state

    def respond(self, _: Event):
        print(self._message, self._state.value())
