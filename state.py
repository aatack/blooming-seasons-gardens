from typing import Any, Callable, Dict, Optional, NamedTuple, Type
from collections import OrderedDict
from inspect import Signature, Parameter, signature
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
            **{key: state.value() for key, state in self._kwargs.items()}
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
        source: State

    class Removed(State.Event, NamedTuple):
        index: int
        value: Optional[Any]
        source: State

    def __init__(self, *elements: State):
        super().__init__()

        self._elements = list(elements)
        self._index = {element: i for i, element in enumerate(self._elements)}

        for element in self._elements:
            self.listen(element)

    def value(self):
        return [element.value() for element in self._elements]

    def respond(self, event: State.Event):
        self.broadcast(self.Index(self._index[event.source], event, self))

    def add(self, state: State):
        event = self.Added(len(self._elements), state.value(), self)
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


class _Decorators:
    class Derived(NamedTuple):
        function: Callable


derive = _Decorators.Derived


def struct(constructor: Type) -> Type:
    attributes = constructor.__dict__

    variables = OrderedDict()
    derived_variables = OrderedDict()
    leftovers = {}

    for key, value in attributes["__annotations__"].items():
        variables[key] = Parameter(
            name=key, annotation=value, kind=Parameter.POSITIONAL_OR_KEYWORD
        )

    for key, value in attributes.items():
        if key.startswith("__"):
            continue

        if isinstance(value, _Decorators.Derived):
            arguments = [
                parameter.name
                for parameter in signature(value.function).parameters.values()
            ]

            for argument in arguments:
                assert argument in variables or argument in derived_variables

            derived_variables[key] = (value.function, arguments)
        elif type(value).__name__ == "function":
            leftovers[key] = value
        else:
            parameter = variables[key]
            variables[key] = Parameter(
                name=key,
                annotation=parameter.annotation,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=value,
            )

    class_signature = Signature(parameters=list(variables.values()))

    def __init__(self, *args, **kwargs):
        Keyed.__init__(self)

        binding = class_signature.bind(*args, **kwargs)
        binding.apply_defaults()

        for attribute, argument in binding.arguments.items():
            self.add(
                attribute,
                argument if isinstance(argument, State) else Variable(argument),
            )

        for attribute, (function, arguments) in derived_variables.items():
            self.add(
                attribute,
                Derived(function, *[self[argument] for argument in arguments]),
            )

    return type(constructor.__name__, (Keyed,), dict(__init__=__init__, **leftovers))
