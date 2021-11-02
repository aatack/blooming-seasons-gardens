from state import State, Keyed, Variable, Derived
from typing import NamedTuple, Callable, Type, Any, Tuple, List
from collections import OrderedDict
from inspect import Signature, Parameter, signature


class _Decorators:
    class Derived(NamedTuple):
        function: Callable

    class Prepared(NamedTuple):
        function: Callable


derive = _Decorators.Derived
prepare = _Decorators.Prepared


class _Definition:
    def __init__(self):
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
        """
        Get the names of the arguments in a function and check that they all exist.
        """
        arguments = [
            parameter.name for parameter in signature(function).parameters.values()
        ]

        for argument in arguments:
            assert self.defines(argument)

        return arguments

    def _attribute(self, attribute: str) -> str:
        """Validate an attribute and check that it does not exist."""
        assert len(attribute) > 0 and attribute[0] != "_"
        assert not self.defines(attribute)
        return attribute

    def parse_constructor(self, constructor: Type):
        attributes = constructor.__dict__

        for key, value in attributes["__annotations__"].items():
            self.provided[self._attribute(key)] = Parameter(
                name=key, annotation=value, kind=Parameter.POSITIONAL_OR_KEYWORD
            )

        for key, value in attributes.items():
            if key.startswith("__"):
                continue

            if isinstance(value, _Decorators.Derived):
                self.derived[self._attribute(key)] = (
                    value.function,
                    self._argument_names(value.function),
                )

            elif isinstance(value, _Decorators.Prepared):
                self.prepared[self._attribute(key)] = (
                    value.function,
                    self._argument_names(value.function),
                )

            elif type(value).__name__ == "function":
                self.leftover[key] = value

            else:
                assert not key.startswith("_")
                parameter = self.provided[key]
                self.provided[key] = Parameter(
                    name=key,
                    annotation=parameter.annotation,
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=value,
                )

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
    definition = _Definition()
    definition.parse_constructor(constructor)

    class_signature = definition.constructor_signature

    def __init__(self, *args, **kwargs):
        Keyed.__init__(self)

        binding = class_signature.bind(*args, **kwargs)
        binding.apply_defaults()

        for attribute, argument in binding.arguments.items():
            self.add(
                attribute,
                argument if isinstance(argument, State) else Variable(argument),
            )

        for attribute, (function, arguments) in definition.derived.items():
            self.add(
                attribute,
                Derived(function, *[self[argument] for argument in arguments]),
            )

        for attribute, (function, arguments) in definition.prepared.items():
            self.add(attribute, function(*[self[argument] for argument in arguments]))

    def __getattr__(self, attribute: str) -> Any:
        return self[attribute].value()

    def __setattr__(self, attribute: str, value: Any):
        # TODO: also check that the current value is a state
        if definition.defines(attribute):
            self[attribute].modify(value)
        else:
            self.__dict__[attribute] = value

    return type(
        constructor.__name__,
        (Keyed,),
        dict(
            __init__=__init__,
            __getattr__=__getattr__,
            __setattr__=__setattr__,
            **definition.leftover
        ),
    )
