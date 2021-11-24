import pygame
from typing import Optional
from state import State, Variable, Derived
from components import Colour, Point
from view import simplify, render


pygame.init()


class Window:
    def __init__(
        self,
        title: Optional[str] = None,
        background_colour: Colour = Colour(red=1.0, green=1.0, blue=1.0),
    ):
        pygame.init()

        self.background_colour = background_colour

        self.title = title
        if self.title is not None:
            pygame.display.set_caption(self.title)

        self.width = Variable(500)
        self.height = Variable(500)

        self.surface = pygame.display.set_mode(
            (self.width.value(), self.height.value()), pygame.RESIZABLE
        )

    def run(self, state: State):
        view = Derived(simplify, state.view())
        while self.loop(state, view):
            pass

    def loop(self, state: State, view: State) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.surface = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                self.width.modify(event.w)
                self.height.modify(event.h)
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                state.key(event.key, True)
            if event.type == pygame.KEYUP:
                state.key(event.key, False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: work out why the position in the event does not match the
                #       position in the stored state if the mouse is clicked while it is
                #       moving
                state.click(event.button, event.pos, True)
            if event.type == pygame.MOUSEBUTTONUP:
                state.click(event.button, event.pos, False)
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                dx, dy = event.rel
                state.mouse(current=(x, y), previous=(x - dx, y - dy), move=(dx, dy))

        self.surface.fill(self.background_colour.colour_cache)
        view_value = view.value()
        if view_value is not None:
            render(view_value, self.surface)

        pygame.display.flip()
        return True
