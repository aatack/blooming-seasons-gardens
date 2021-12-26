from trickle import Keyed

from garden.element import Element


class Garden(Keyed):
    def __init__(self, element: Element):
        super().__init__(element=element)

    @property
    def element(self) -> Element:
        return self["element"]
