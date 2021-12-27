from components.component import Anonymous, Component
from components.positioning import Move
from settings import EDITOR_WIDTH
from trickle import Derived, Keyed, Overlay

from garden.element import Element


class Garden(Keyed):
    def __init__(self, element: Element):
        super().__init__(element=element)

    @property
    def element(self) -> Element:
        return self["element"]

    @property
    def component(self) -> Component:
        return Anonymous(
            lambda environment: Derived(
                lambda p, e: Overlay(p, e),
                Move(
                    self.element.plan,
                    horizontal=environment.screen.width * EDITOR_WIDTH,
                )(environment),
                self.element.editor(
                    environment.where(
                        screen=environment.screen.resize(
                            width=environment.screen.width * EDITOR_WIDTH
                        )
                    )
                ),
            )
        )
