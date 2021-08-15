from typing import Dict, Any, NamedTuple, Type, Optional, Callable, List
from wrapper.renderable import Renderable, Void
import pygame
import inspect


class Scrap:
    _DEFINITION: "Definition"

    def __init__(self, *args, **kwargs):
        self._latent = _resolve_arguments(args, kwargs, self._DEFINITION.latent)
        self._derived: Dict[str, Any] = {}

    def __getattr__(self, attribute: str) -> Any:
        # Assume attribute has at least one character
        if attribute[0].islower():
            try:
                if attribute in self._latent:
                    return self._latent[attribute]
                if attribute not in self._derived:
                    self._derived[attribute] = self._DEFINITION.derived[attribute](self)
                return self._derived[attribute]
            except KeyError:
                raise AttributeError(f"No attribute {attribute} on {self}")

        if attribute[0].isupper():
            return lambda *args, **kwargs: self._handle(
                getattr(Registry, attribute)(*args, **kwargs)
            )

        raise AttributeError(attribute)

    def _handle(self, event: "Scrap") -> "Scrap":
        assert isinstance(event, Scrap)
        if isinstance(event, Registry.get("Void")):
            return self

        preprocessed_event = _identity(self._DEFINITION.handlers.preprocessor)(
            self, event
        )
        handling_function = self._DEFINITION.handlers.specific.get(
            preprocessed_event._DEFINITION.name,
            _identity(self._DEFINITION.handlers.fallback),
        )
        result = _identity(self._DEFINITION.handlers.postprocessor)(
            self, handling_function(self, preprocessed_event),
        )
        assert isinstance(result, Scrap)
        return result

    def _cache(self) -> Renderable:
        """Return a cached version of the rendered view of this scrap."""
        return Void()

    def _render(self, surface: pygame.Surface):
        """Render the scrap to a pygame surface."""
        self.cache().render(surface)

    def __str__(self) -> str:
        return (
            self._DEFINITION.name
            + "("
            + ", ".join(
                [f"{name}={self._latent[name]}" for name, *_ in self._DEFINITION.latent]
            )
            + ")"
        )


class Builder(type):
    def __getattr__(cls, attribute: str) -> Any:
        constructor = cls._CONSTRUCTOR_LOOKUP[attribute]
        return constructor


class Registry(metaclass=Builder):

    _CONSTRUCTOR_LOOKUP: Dict[str, Type[Scrap]] = {}
    _ALLOW_DEFINITIONS: bool = False

    @classmethod
    def get(cls, name: str) -> Type[Scrap]:
        return cls._CONSTRUCTOR_LOOKUP[name]

    @classmethod
    def register(cls, definition: "Definition"):
        constructor = constructor_from_definition(definition)
        # TODO: assert that registrations are allowed
        assert issubclass(constructor, Scrap)
        assert definition.name != "Scrap"
        assert definition.name not in cls._CONSTRUCTOR_LOOKUP
        cls._CONSTRUCTOR_LOOKUP[definition.name] = constructor

    @classmethod
    def verify(cls):
        def assert_valid_name(
            candidate: str, *, lower: bool = False, upper: bool = False
        ):
            assert isinstance(candidate, str)
            assert len(candidate) > 0
            character = candidate[0]
            assert character.isidentifier()
            assert character != "_"
            if lower:
                assert character.islower()
            if upper:
                assert character.isupper()

        for name, constructor in cls._CONSTRUCTOR_LOOKUP.items():
            assert_valid_name(name, upper=True)
            definition = constructor._DEFINITION
            assert definition.name == name

            requires_default = False
            for latent in definition.latent:
                assert_valid_name(latent.name, lower=True)
                if requires_default:
                    assert latent.optional
                if latent.optional:
                    requires_default = True

            for handler in definition.handlers.specific.keys():
                cls.get(handler)  # Throws error if the handler does not exist


Handler = Callable[[Scrap, Scrap], Scrap]
Derived = Callable[[Scrap], Scrap]


class Latent(NamedTuple):
    name: str
    kind: Type
    optional: bool
    default: Optional[Any]


class Handlers(NamedTuple):
    preprocessor: Optional[Handler]
    specific: Dict[str, Handler]
    fallback: Optional[Handler]
    postprocessor: Optional[Handler]


class Definition(NamedTuple):
    name: str
    latent: List[Latent]
    derived: Dict[str, Derived]
    handlers: Handlers
    cache: Optional[Callable[[], Renderable]]
    render: Optional[Callable[[pygame.Surface], None]]


def definition_from_constructor(constructor: Type) -> Definition:
    attributes = constructor.__dict__

    derived = {}
    specific = {}

    latent = [
        Latent(
            name,
            annotation,
            name in constructor.__dict__,
            constructor.__dict__.get(name),
        )
        for name, annotation in attributes.get("__annotations__", {}).items()
    ]
    skip = {name for name, *_ in latent}

    for key, value in attributes.items():
        if key.startswith("__") or key in skip:
            continue

        if key[0].islower():
            assert (
                type(value).__name__ == "function"
            ), f"Missing type annotation for {key}"
            derived[key] = value

        if key[0].isupper():
            assert type(value).__name__ == "function"
            specific[key] = _unpack_scrap(value)

    return Definition(
        constructor.__name__,
        latent,
        derived,
        Handlers(
            attributes.get("_preprocessor", None),
            specific,
            attributes.get("_fallback", None),
            attributes.get("_postprocessor", None),
        ),
        attributes.get("_cache", None),
        attributes.get("_render", None),
    )


def constructor_from_definition(definition: Definition) -> Type:
    attributes = {"_DEFINITION": definition}

    if definition.cache is not None:
        attributes["_cache"] = definition.cache

    if definition.render is not None:
        attributes["_render"] = definition.cache

    return type(definition.name, (Scrap,), attributes)


def defscrap(constructor: Type) -> Type[Scrap]:
    definition = definition_from_constructor(constructor)
    Registry.register(definition)
    return Registry.get(definition.name)


def _resolve_arguments(
    args: tuple, kwargs: dict, latent: List[Latent]
) -> Dict[str, Any]:
    arguments = {}

    for i, (name, _, optional, default) in enumerate(latent):
        if i < len(args):
            arguments[name] = args[i]
            assert name not in kwargs
        else:
            if not optional:
                raise ValueError(f"Required argument {name} missing")
            arguments[name] = kwargs.get(name, default)

    return arguments


def _identity(
    function: Optional[Callable[[Any, Any], Any]]
) -> Callable[[Any, Any], Any]:
    return function if function is not None else (lambda self, _: self)


def _unpack_scrap(function: Callable[..., Scrap]) -> Callable[[Scrap, Scrap], Scrap]:
    """
    Decorate a function so that it unpacks any scraps passed to it.
    
    More specifically, the input function should be a function that takes a `self` scrap
    as well as any number of arguments that should be unpacked from another scrap.  A
    function will be returned which takes a `self` scrap and an `other` scrap; the
    arguments will be inferred from the `other` scrap and passed to the underlying
    function, whose result will then be returned unmodified.
    """
    spec = inspect.getfullargspec(function)

    assert len(spec.args) > 0 and spec.args[0] == "self"
    assert spec.varargs is None
    assert spec.varkw is None
    assert spec.defaults is None
    assert spec.kwonlyargs == []
    assert spec.kwonlydefaults is None

    ellipses_annotations = {
        key for key, value in spec.annotations.items() if value is ...
    }
    required_arguments = {
        argument for argument in spec.args[1:] if argument not in ellipses_annotations
    }

    def wrapped_function(self: Scrap, other: Scrap) -> Scrap:
        arguments = {
            argument: getattr(other, argument) for argument in required_arguments
        }
        for argument in ellipses_annotations:
            arguments[argument] = other
        return function(self, **arguments)

    return wrapped_function
