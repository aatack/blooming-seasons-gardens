from collections import OrderedDict
from inspect import Parameter, Signature, signature
from typing import Any, Callable, List, NamedTuple, Tuple, Type

from state import Derived, Dict, Keyed, State, Variable


class _Struct:
    """Empty class for setting attributes in struct values."""


class Struct(Keyed):
    """Empty class for `issubclass` checks."""

    def value(self):
        value_disctionary = super().value()
        value_object = _Struct()

        for key, value in value_disctionary.items():
            setattr(value_object, key, value)

        return value_object


class _Decorators:
    class Derived(NamedTuple):
        function: Callable

    class Prepared(NamedTuple):
        function: Callable


derive = _Decorators.Derived
prepare = _Decorators.Prepared


class _Definition:
    def __init__(self):
        self.order: List[str] = []
        self.provided: Dict[str, Parameter] = OrderedDict()
        self.derived: Dict[str, Tuple[Callable, List[str]]] = OrderedDict()
        self.prepared: Dict[str, Tuple[Callable, List[str]]] = OrderedDict()
        self.leftover: Dict[str, Callable] = OrderedDict()

    def defines(self, attribute: str) -> bool:
        return (
            (attribute in self.provided)
            or (attribute in self.derived)
            or (attribute in self.prepared)
        )

    def _argument_names(self, function: Callable) -> List[str]:
        """Get the names of the arguments in a function."""
        return [parameter.name for parameter in signature(function).parameters.values()]

    def _attribute(self, attribute: str) -> str:
        """Validate an attribute and check that it does not exist."""
        assert len(attribute) > 0 and attribute[0] != "_"
        assert not self.defines(attribute), f"{attribute} is defined twice"
        return attribute

    def parse_constructor(self, constructor: Type):
        attributes = constructor.__dict__

        for attribute, value in attributes.get("__annotations__", {}).items():
            _attribute = self._attribute(attribute)
            self.provided[_attribute] = Parameter(
                name=attribute, annotation=value, kind=Parameter.POSITIONAL_OR_KEYWORD
            )
            # self.order.append(_attribute)

        for attribute, value in attributes.items():
            if attribute.startswith("__") or attribute == "_abc_impl":
                continue

            if isinstance(value, _Decorators.Derived):
                _attribute = self._attribute(attribute)
                self.derived[_attribute] = (
                    value.function,
                    self._argument_names(value.function),
                )
                self.order.append(_attribute)

            elif isinstance(value, _Decorators.Prepared):
                _attribute = self._attribute(attribute)
                self.prepared[_attribute] = (
                    value.function,
                    self._argument_names(value.function),
                )
                self.order.append(_attribute)

            elif type(value).__name__ == "function":
                self.leftover[attribute] = value

            else:
                parameter = self.provided[attribute]
                self.provided[attribute] = Parameter(
                    name=attribute,
                    annotation=parameter.annotation,
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=value,
                )

    def parse_parent(self, parent: "_Definition"):
        for attribute, value in parent.provided.items():
            if not self.defines(attribute):
                self.provided[attribute] = value

        for attribute, value in parent.derived.items():
            if not self.defines(attribute):
                self.derived[attribute] = value

        for attribute, value in parent.prepared.items():
            if not self.defines(attribute):
                self.prepared[attribute] = value

        for attribute in parent.order:
            self.order.append(attribute)

    @property
    def sorted_provided(self) -> List[Parameter]:
        """Sort provided variables such that those with default values come last."""
        return [p for p in self.provided.values() if p.default is Parameter.empty] + [
            p for p in self.provided.values() if p.default is not Parameter.empty
        ]

    @property
    def constructor_signature(self) -> Signature:
        return Signature(parameters=self.sorted_provided)


def struct(constructor: Type) -> Type:
    bases = [base for base in constructor.__bases__ if base is not object]

    definition = _Definition()
    definition.parse_constructor(constructor)
    for base in bases:
        assert issubclass(base, Struct)
        definition.parse_parent(base._definition)

    class_signature = definition.constructor_signature

    def __init__(self, *args, **kwargs):
        Struct.__init__(self)

        # TODO: add a private variable that creates an instance of each struct from
        #       which this struct inherits, to allow for casting (and to solve any
        #       ambiguity that might arise)

        binding = class_signature.bind(*args, **kwargs)
        binding.apply_defaults()

        for attribute, argument in binding.arguments.items():
            self.add(
                attribute,
                argument if isinstance(argument, State) else Variable(argument),
            )

        order = set(definition.order)
        while len(order) > 0:
            current = list(order)
            current_length = len(current)

            for attribute in current:
                try:
                    if attribute in definition.derived:
                        function, arguments = definition.derived[attribute]
                        self.add(
                            attribute,
                            Derived(
                                function, *[self[argument] for argument in arguments]
                            ),
                        )

                    if attribute in definition.prepared:
                        function, arguments = definition.prepared[attribute]
                        self.add(
                            attribute,
                            function(*[self[argument] for argument in arguments]),
                        )

                    order.remove(attribute)
                except KeyError:
                    pass

            assert len(order) < current_length

    def __getattr__(self, attribute: str) -> Any:
        return self[attribute].value()

    def __setattr__(self, attribute: str, value: Any):
        # TODO: also check that the current value is a state
        if definition.defines(attribute):
            self[attribute].modify(value)
        else:
            self.__dict__[attribute] = value

    if definition.defines("view") and "view" not in definition.leftover:
        # This allows the view to be defined as a derived or prepared state, but also
        # does not prevent it from being overridden by subclasses as a leftover
        definition.leftover["view"] = lambda self: self["view"]

    struct_constructor = type(
        constructor.__name__,
        # TODO: this should probably use all bases instead of just the first one, since
        #       they are all parsed into the descriptor
        (Struct if len(bases) == 0 else bases[0],),
        dict(
            __init__=__init__,
            __getattr__=__getattr__,
            __setattr__=__setattr__,
            **definition.leftover,
        ),
    )
    struct_constructor._definition = definition
    return struct_constructor
