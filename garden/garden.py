from trickle import Keyed

from garden.element import Element


class Garden(Keyed):
    def __init__(self, garden: Element):
        super().__init__(garden=garden)

    @property
    def garden(self) -> Element:
        return self["garden"]
