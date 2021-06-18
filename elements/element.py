import abc
from utils.serialisation import serialise_path, deserialise_path
from typing import Optional, Union


JSON = Optional[Union[dict, list, int, float, str, bool]]


class Element(abc.ABC):
    """A base class for any element of a garden that can be rendered in a plan."""

    def serialise(self) -> JSON:
        return {
            "type": serialise_path(type(self)),
            "data": self._serialise(),
        }

    @abc.abstractmethod
    def _serialise(self) -> JSON:
        """Serialise the element to a JSON-like object."""

    @classmethod
    def deserialise(cls, json: JSON) -> "Element":
        return deserialise_path(json["type"])._deserialise(json["data"])

    @classmethod
    @abc.abstractmethod
    def _deserialise(cls, json: JSON) -> "Element":
        """Deserialise an instance of this element type from a JSON-like object."""

    def copy(self) -> "Element":
        return self.deserialise(self.serialise())
