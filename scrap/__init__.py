from typing import Dict, Any, NamedTuple, Type, Optional, Callable, List


class Scrap:
    _DEFINITION: "Definition"

    def __init__(self, latent: Dict[str, Any]):
        self._latent = latent
        self._derived: Dict[str, Any] = {}

    def __getattr__(self, attribute: str) -> Any:
        # Assume attribute has at least one character
        if attribute[0].islower():
            if attribute in self._latent:
                return self._latent[attribute]
            if attribute not in self._derived:
                self._derived[attribute] = self._DEFINITION.derived[attribute]
            return self._derived[attribute]

        if attribute[0].isupper():
            raise NotImplementedError()

        raise AttributeError(attribute)


Handler = Callable[[Scrap, Scrap], Scrap]
Derived = Callable[[Scrap], Scrap]


class Latent(NamedTuple):
    name: str
    kind: Type
    default: Optional[Any]


class Handlers(NamedTuple):
    preprocessor: Optional[Handler]
    specific: Dict[str, Handler]
    fallback: Optional[Handler]
    postprocessor: Optional[Handler]


class Definition(NamedTuple):
    latent: List[Latent]
    derived: Dict[str, Derived]
    handlers: Handlers


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
