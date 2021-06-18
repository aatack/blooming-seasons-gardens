from typing import Type
from pydoc import locate


def serialise_path(constructor: Type) -> str:
    return constructor.__module__ + "." + constructor.__qualname__


def deserialise_path(constructor: str) -> Type:
    return locate(constructor)
