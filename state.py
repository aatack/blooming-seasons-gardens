from typing import Any, Callable, Dict, List, Optional, NamedTuple
import abc


class State(abc.ABC):
    class Event(NamedTuple):
        source: "State"

    def __init__(self):
        self._listeners: Dict[State, int] = {}

    @abc.abstractmethod
    def value(self) -> Any:
        """Return the current value of the state."""

    @abc.abstractmethod
    def respond(self, event: Event):
        """Respond to an event caused by a state to which this state is listening."""

    def view(self) -> "State":
        """Optionally, return a state containing a view for rendering."""
        return Constant(None)  # TODO: ensure this can be properly cached

    def listen(self, state: "State"):
        """Denote that this state should receive broadcasts from another one."""
        # TODO: check for cyclic dependencies
        if self not in state._listeners:
            state._listeners[self] = 0
        state._listeners[self] += 1

    def ignore(self, state: "State"):
        """Stop listening for events caused by the given state."""
        assert self in state._listeners, "The given state is not being listened for"
        state._listeners[self] -= 1
        if state._listeners[self] == 0:
            # TODO: is this sufficient garbage collection?
            del state._listeners[self]

    def broadcast(self, event: "State.Event"):
        """Called whenever an event happens which changes the state's value."""
        assert event.source is self, "States can only broadcast events about themselves"
        for state in self._listeners.keys():
            state.respond(event)

    def log(self) -> "State":
        _ = _Log(self)
        return self


class Constant(State):
    def __init__(self, value: Any):
        super().__init__()
        self._value = value

    def value(self) -> Any:
        return self._value

    def respond(self):
        pass


class Variable(State):
    class Modified(State.Event, NamedTuple):
        old: Optional[Any]
        new: Optional[Any]
        source: State

    def __init__(self, value: Optional[Any] = None):
        super().__init__()
        self._value = value

    def value(self) -> Optional[Any]:
        return self._value

    def respond(self, event: State.Event):
        pass

    def modify(self, new: Optional[Any]):
        event = self.Modified(self._value, new, self)
        self._value = new
        if event.old != event.new:
            self.broadcast(event)


class Derived(State):
    class Changed(State.Event, NamedTuple):
        old: Optional[Any]
        new: Optional[Any]
        source: State

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
            **{key: state.value() for key, state in self._kwargs.items()},
        )

    def respond(self, event: State.Event):
        event = self.Changed(self._value, self._compute(), self)
        self._value = event.new
        if event.old != event.new:
            self.broadcast(event)


class Ordered(State):
    class Index(State.Event, NamedTuple):
        index: int
        event: State.Event
        source: State

    class Added(State.Event, NamedTuple):
        index: int
        value: Optional[Any]
        element: State
        source: State

    class Removed(State.Event, NamedTuple):
        index: int
        value: Optional[Any]
        source: State

    def __init__(self, *elements: State):
        super().__init__()

        self._elements: List[State] = []
        self._index: Dict[State, int] = {}

        for element in elements:
            self.add(element)

    def value(self):
        return [element.value() for element in self._elements]

    def respond(self, event: State.Event):
        self.broadcast(self.Index(self._index[event.source], event, self))

    def view(self) -> Optional[State]:
        raise NotImplementedError()

    def add(self, state: State):
        event = self.Added(len(self._elements), state.value(), state, self)
        self._elements.append(state)
        self._index[state] = event.index
        self.listen(state)
        self.broadcast(event)

    def remove(self, index: int):
        state = self._elements[index]
        del self._elements[index]
        del self._index[state]
        for element, i in self._index.items():
            if i > index:
                self._index[element] -= 1
        self.ignore(state)
        self.broadcast(self.Removed(index, state.value(), self))

    def __getitem__(self, index: int) -> State:
        return self._elements[index]


class Mapped(Ordered):
    def __init__(self, source: Ordered, function: Callable[[State], State]):
        self._source = source
        self._function = function

        self.listen(self._source)

        super().__init__(*self._source._elements)

    def respond(self, event: State.Event):
        if event.source is self._source:
            if isinstance(event, Ordered.Index):
                pass  # This can be ignored as it will be handled by the child
            elif isinstance(event, Ordered.Added):
                self.add(event.element)
            elif isinstance(event, Ordered.Removed):
                self.remove(event.index)
            else:
                raise ValueError(f"Unknown ordered event: {event}")
        else:
            super().respond(event)  # Handle events for individual children

    def add(self, state: State):
        state = self._function(state)
        self.listen(state)
        event = self.Added(len(self._elements), state.value(), state, self)
        self._elements.append(state)
        self._index[state] = event.index
        self.broadcast(event)

    def remove(self, index: int):
        state = self._elements[index]
        del self._elements[index]
        del self._index[state]
        for element, i in self._index.items():
            if i > index:
                self._index[element] -= 1
        self.ignore(state)  # TODO: this may leave hanging references
        self.broadcast(self.Removed(index, state.value(), self))


class Keyed(State):
    class Key(State.Event, NamedTuple):
        key: str
        event: State.Event
        source: State

    class Added(State.Event, NamedTuple):
        key: str
        value: Optional[Any]
        source: State

    class Removed(State.Event, NamedTuple):
        key: str
        value: Optional[Any]
        source: State

    def __init__(self, **elements: State):
        super().__init__()

        self._elements = elements
        self._key = {element: key for key, element in self._elements.items()}

        for element in self._elements.values():
            self.listen(element)

    def value(self):
        return {key: element.value() for key, element in self._elements.items()}

    def respond(self, event: State.Event):
        self.broadcast(self.Key(self._key[event.source], event, self))

    def add(self, key: str, state: State):
        assert key not in self._elements
        event = self.Added(key, state.value(), self)
        self._elements[key] = state
        self._key[state] = key
        self.listen(state)
        self.broadcast(event)

    def remove(self, key: str):
        state = self._elements[key]
        del self._elements[key]
        del self._key[state]
        self.ignore(state)
        self.broadcast(self.Removed(key, state.value(), self))

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

    def respond(self, _: State.Event):
        print(self._message, self._state.value())
