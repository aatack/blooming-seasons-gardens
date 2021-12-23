from typing import Union

from garden.element import Element
from garden.environment import Environment
from trickle.trickles.puddle import Puddle


class Plant(Element):
    def __init__(
        self,
        name: Union[Puddle, str],
        size: Union[Puddle, float],
        horizontal: Union[Puddle, float] = 0.0,
        vertical: Union[Puddle, float] = 0.0,
    ):
        super().__init__(name=name, size=size, horizontal=horizontal, vertical=vertical)

    @property
    def name(self) -> Puddle:
        return self["name"]

    @property
    def size(self) -> Puddle:
        return self["size"]

    @property
    def horizontal(self) -> Puddle:
        return self["horizontal"]

    @property
    def vertical(self) -> Puddle:
        return self["vertical"]

    def plan(self, environment: Environment) -> Puddle:
        raise NotImplementedError()
