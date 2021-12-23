from typing import List, Union

from garden.element import Element
from garden.environment import Environment
from trickle import Indexed
from trickle.trickles.puddle import Puddle


class Bed(Element):
    def __init__(
        self,
        elements: List[Element],
        horizontal: Union[float, Puddle] = 0.0,
        vertical: Union[float, Puddle] = 0.0,
    ):
        assert isinstance(elements, List)
        for element in elements:
            assert isinstance(element, Element)

        super().__init__(
            elements=Indexed(*elements), horizontal=horizontal, vertical=vertical,
        )

    @property
    def elements(self) -> Indexed:
        elements = self["elements"]
        assert isinstance(elements, Indexed)
        return elements

    def plan(self, environment: Environment) -> Puddle:
        raise NotImplementedError()
