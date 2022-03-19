from components.component import Anonymous, Component
from components.positioning import Move, Scroll
from components.presentation import Background, Fill
from settings import EDITOR_BACKGROUND_COLOUR, EDITOR_SCROLL_SPEED, EDITOR_WIDTH
from trickle import Derived, Keyed, Overlay, environment

from garden.element import Element


class Garden(Keyed):
    def __init__(self, element: Element):
        super().__init__(element=element)

    @property
    def element(self) -> Element:
        return self["element"]

    @property
    def component(self) -> Component:
        def component(environment: environment.Environment) -> Derived:
            plan = Move(
                self.element.plan,
                horizontal=environment.screen.width * EDITOR_WIDTH,
            )
            editor = Background(
                Fill(Scroll(self.element.editor, scroll_speed=EDITOR_SCROLL_SPEED)),
                EDITOR_BACKGROUND_COLOUR,
            )

            return Derived(
                lambda p, e: Overlay(p, e),
                plan(environment),
                editor(
                    environment.where(
                        screen=environment.screen.resize(
                            width=environment.screen.width * EDITOR_WIDTH
                        )
                    )
                ),
            )

        # TODO: implement this as a component directly
        return Anonymous(component)
