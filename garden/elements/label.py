from typing import Union

from garden.element import Element
from trickle.trickles.puddle import Puddle


class Label(Element):
    def __init__(
        self,
        text: Union[str, Puddle],
        size: Union[int, Puddle],
        horizontal: Union[float, Puddle],
        vertical: Union[float, Puddle],
    ):
        super().__init__(text=text, size=size, horizontal=horizontal, vertical=vertical)

    @property
    def text(self) -> Puddle:
        return self["text"]

    @property
    def size(self) -> Puddle:
        return self["size"]

    @property
    def horizontal(self) -> Puddle:
        return self["horizontal"]

    @property
    def vertical(self) -> Puddle:
        return self["vertical"]
