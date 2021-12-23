from typing import Union

from garden.element import Element
from garden.environment import Environment
from trickle.trickles.puddle import Puddle


class Arrow(Element):
    def __init__(
        self,
        start_horizontal: Union[float, Puddle],
        start_vertical: Union[float, Puddle],
        end_horizontal: Union[float, Puddle],
        end_vertical: Union[float, Puddle],
    ):
        super().__init__(
            start_horizontal=start_horizontal,
            start_vertical=start_vertical,
            end_horizontal=end_horizontal,
            end_vertical=end_vertical,
        )

    @property
    def start_horizontal(self) -> Puddle:
        return self["start_horizontal"]

    @property
    def start_vertical(self) -> Puddle:
        return self["start_vertical"]

    @property
    def end_horizontal(self) -> Puddle:
        return self["end_horizontal"]

    @property
    def end_vertical(self) -> Puddle:
        return self["end_vertical"]

    def plan(self, environment: Environment) -> Puddle:
        raise NotImplementedError()
