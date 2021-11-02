from state import State, Keyed, Variable, Derived
from typing import NamedTuple, Callable, Type, Any
from collections import OrderedDict
from inspect import Signature, Parameter, signature


class _Decorators:
    class Derived(NamedTuple):
        function: Callable

    class Prepared(NamedTuple):
        function: Callable


derive = _Decorators.Derived
prepare = _Decorators.Prepared


def struct(constructor: Type) -> Type:
    attributes = constructor.__dict__

    variables = OrderedDict()
    derived_variables = OrderedDict()
    prepared_variables = OrderedDict()
    leftovers = {}

    for key, value in attributes["__annotations__"].items():
        assert not key.startswith("_")
        variables[key] = Parameter(
            name=key, annotation=value, kind=Parameter.POSITIONAL_OR_KEYWORD
        )

    for key, value in attributes.items():
        if key.startswith("__"):
            continue

        if isinstance(value, _Decorators.Derived):
            assert not key.startswith("_")
            arguments = [
                parameter.name
                for parameter in signature(value.function).parameters.values()
            ]

            for argument in arguments:
                assert argument in variables or argument in derived_variables

            derived_variables[key] = (value.function, arguments)

        elif isinstance(value, _Decorators.Prepared):
            assert not key.startswith("_")
            arguments = [
                parameter.name
                for parameter in signature(value.function).parameters.values()
            ]

            for argument in arguments:
                assert argument in variables or argument in derived_variables

            prepared_variables[key] = (value.function, arguments)

        elif type(value).__name__ == "function":
            leftovers[key] = value

        else:
            assert not key.startswith("_")
            parameter = variables[key]
            variables[key] = Parameter(
                name=key,
                annotation=parameter.annotation,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=value,
            )

    # Sort variables such that those with defaults always come last
    sorted_variables = [
        p for p in variables.values() if p.default is Parameter.empty
    ] + [p for p in variables.values() if p.default is not Parameter.empty]

    class_signature = Signature(parameters=sorted_variables)

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

        for attribute, (function, arguments) in prepared_variables.items():
            self.add(attribute, function(*[self[argument] for argument in arguments]))

    def __getattr__(self, attribute: str) -> Any:
        return self[attribute].value()

    def __setattr__(self, attribute: str, value: Any):
        # TODO: also check that the current value is a state
        if attribute in variables or attribute in derived_variables:
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
            **leftovers
        ),
    )