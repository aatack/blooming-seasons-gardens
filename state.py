import abc
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple


class State(abc.ABC):
    class Event(NamedTuple):
        source: "State"

    def __init__(self):
        self._listeners: Dict[State, int] = {}

    @abc.abstractmethod
    def value(self) -> Any:
        """Return the current value of the state."""

    @abc.abstractmethod
    def respond(self, event: "State.Event"):
        """Respond to an event caused by a state to which this state is listening."""

    def render(
        self, screen: "Screen", mouse: "Mouse", keyboard: "Keyboard"
    ) -> "Rendered":
        """Return a state containing a view for rendering."""
        raise NotImplementedError(
            f"States of type {type(self).__name__} cannot be rendered"
        )

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

    def __add__(self, other: Any) -> "State":
        return Derived(lambda left, right: left + right, self, other)

    def __radd__(self, other: Any) -> "State":
        return type(self).__add__(other, self)

    def __mul__(self, other: Any) -> "State":
        return Derived(lambda left, right: left * right, self, other)

    def __rmul__(self, other: Any) -> "State":
        return type(self).__mul__(other, self)

    def __sub__(self, other: Any) -> "State":
        return Derived(lambda left, right: left - right, self, other)

    def __rsub__(self, other: Any) -> "State":
        return type(self).__sub__(other, self)

    def __truediv__(self, other: Any) -> "State":
        return Derived(lambda left, right: left / right, self, other)

    def __rtruediv__(self, other: Any) -> "State":
        return type(self).__truediv__(other, self)


class Rendered(State):
    def __init__(
        self,
        view: State,
        source: State,
        width: Optional[State] = None,
        height: Optional[State] = None,
    ):
        super().__init__()

        self.view = view
        self.source = source

        self.width = width
        self.height = height

        if self.width is None:
            import view as _view

            self.width = Derived(_view.width, self.view)

        if self.height is None:
            import view as _view

            self.height = Derived(_view.height, self.height)

    def value(self) -> Any:
        # TODO: possibly assert that the value is an instance of view.View
        return self.view.value()

    def respond(self, _: State.Event):
        """Do nothing, as the view should react of its own accord."""

    def render(self, screen: "Screen", mouse: "Mouse", keyboard: "Keyboard") -> "State":
        # TODO: this could potentially just call self.source.render(...) again
        raise NotImplementedError("Rendered states cannot be rendered again")

    def simplify(self) -> "Rendered":
        from view import simplify

        return Rendered(
            Derived(simplify, self.view),
            self.source,
            width=self.width,
            height=self.height,
        )


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
        self._args = tuple(
            arg if isinstance(arg, State) else Variable(arg) for arg in args
        )
        self._kwargs = {
            key: arg if isinstance(arg, State) else Variable(arg)
            for key, arg in kwargs.items()
        }

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

    def key(self, key: int, down: bool):
        for element in self._elements:
            element.key(key, down)

    def click(self, button: int, position: Tuple[int, int], down: bool):
        for element in self._elements:
            element.click(button, position, down)

    def mouse(
        self, current: Tuple[int, int], previous: Tuple[int, int], move: Tuple[int, int]
    ):
        for element in self._elements:
            element.mouse(current, previous, move)


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


class Folded(Ordered):
    def __init__(
        self,
        initial: State,
        source: Ordered,
        fold: Callable[[State, State], Tuple[State, State]],
    ):
        """
        Perform a fold operation over an ordered group of states.

        The folding function should take in the current state and the next element, and
        should output the updated state as well as the transformed element for that
        index.  An initial state must also be given.
        """
        self._initial = initial
        self._source = source
        self._fold = fold

        super().__init__()

        self._steps = []

        self.listen(self._source)
        for state in self._source._elements:
            self.add(state)

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
        step, state = self._fold(
            self._steps[-1] if len(self._steps) > 0 else self._initial, state
        )
        self.listen(state)  # TODO: why does it need to listen to this?
        event = self.Added(len(self._elements), state.value(), state, self)
        self._elements.append(state)
        self._index[state] = event.index
        self._steps.append(step)
        self.broadcast(event)

    def remove(self, index: int):
        # TODO: this is terribly slow and should be rewritten more efficiently; it will
        #       likely leave a bunch of dangling states that don't get garbage collected
        while len(self._elements) > index:
            super().remove(index)
            del self._steps[index]
        for state in self._source._elements[index:]:
            self.add(state)


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


class Mouse(Ordered):
    class Click(State.Event, NamedTuple):
        source: "Mouse"
        button: int
        position: Tuple[int, int]
        down: bool

    def __init__(self, x: State, y: State):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def click(self, button: int, position: Tuple[int, int], down: bool):
        """Broadcast a click event from the mouse."""
        self.broadcast(Mouse.Click(self, button, position, down))


class Keyboard(Constant):
    class Key(State.Event, NamedTuple):
        source: "Keyboard"
        key: int
        down: bool

    def __init__(self):
        super().__init__(None)

    def key(self, key: int, down: bool):
        """Broadcast a key event for the keyboard."""
        self.broadcast(Keyboard.Key(self, key, down))


class Screen(Ordered):
    def __init__(self, width: State, height: State):
        super().__init__(width, height)
        self.width = width
        self.height = height

    def resize(self, width: int, height: int):
        """Resize the screen to a particular width and height."""
        assert isinstance(self.width, Variable)
        self.width.modify(width)

        assert isinstance(self.height, Variable)
        self.height.modify(height)
