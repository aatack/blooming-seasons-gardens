from typing import Dict, Any, NamedTuple, Type, Optional, Callable, List
from wrapper.renderable import Renderable, Void
import pygame


class Scrap:
    _DEFINITION: "Definition"

    def __init__(self, **latent: Dict[str, Any]):
        self._latent = latent
        self._derived: Dict[str, Any] = {}

    def __getattr__(self, attribute: str) -> Any:
        # Assume attribute has at least one character
        if attribute[0].islower():
            if attribute in self._latent:
                return self._latent[attribute]
            if attribute not in self._derived:
                self._derived[attribute] = self._DEFINITION.derived[attribute](self)
            return self._derived[attribute]

        if attribute[0].isupper():
            raise NotImplementedError()

        raise AttributeError(attribute)

    def _handle(self, event: "Scrap") -> "Scrap":
        if isinstance(event, Registry.get("Void")):
            return self

        preprocessed_event = self._DEFINITION.handlers.preprocessor(event)
        return self._DEFINITION.handlers.postprocessor(
            self._DEFINITION.handlers.specific.get(
                type(preprocessed_event), self._DEFINITION.handlers.fallback
            )(preprocessed_event)
        )

    def _cache(self) -> Renderable:
        """Return a cached version of the rendered view of this scrap."""
        return Void()

    def _render(self, surface: pygame.Surface):
        """Render the scrap to a pygame surface."""
        self.cache().render(surface)


class Registry:
    _CONSTRUCTOR_LOOKUP: Dict[str, Type[Scrap]] = {}
    _ALLOW_DEFINITIONS: bool = False

    @classmethod
    def get(cls, name: str) -> Type[Scrap]:
        return cls._CONSTRUCTOR_LOOKUP[name]

    @classmethod
    def register(cls, name: str, constructor: Type[Scrap]):
        # TODO: assert that registrations are allowed
        assert issubclass(constructor, Scrap)
        assert name not in cls._CONSTRUCTOR_LOOKUP
        cls._CONSTRUCTOR_LOOKUP[name] = constructor

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


def definition_from_constructor(constructor: Type) -> Definition:
    pass


def constructor_from_definition(definition: Definition) -> Type:
    return type(definition.name, (Scrap,), {"_DEFINITION": definition})


# from utils.serialisation import deserialise_path as _deserialise
# from scrap.base import Scrap as _Scrap
# from os import listdir as _listdir


# _SCRAP_PATH = "scrap"


# for _file in _listdir(_SCRAP_PATH):
#     if not _file.endswith(".py") or _file.startswith("__"):
#         continue

#     _loaded_module = _deserialise(_SCRAP_PATH + "." + _file.rstrip(".py"))

#     for _attribute in dir(_loaded_module):
#         _constructor = getattr(_loaded_module, _attribute)
#         if isinstance(_constructor, type) and issubclass(_constructor, _Scrap):
#             globals()[_attribute] = _constructor
