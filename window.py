import pygame
from typing import Optional
from state import State, Variable, Derived
from components import Colour, Point
from view import simplify, render


pygame.init()


class Window:
    def __init__(
        self,
        state: Optional[State] = None,
        width: int = 500,
        height: int = 500,
        background_colour: Colour = Colour(red=1.0, green=1.0, blue=1.0),
        title: Optional[str] = None,
    ):
        pygame.init()

        self.state = state
        self.view = Derived(simplify, self.state.view())
        self.background_colour = background_colour

        self.width = Variable(width)
        self.height = Variable(height)
        self.mouse = Point(0, 0)

        self.surface = pygame.display.set_mode(
            (self.width.value(), self.height.value()), pygame.RESIZABLE
        )

        self.title = title
        if self.title is not None:
            pygame.display.set_caption(self.title)

    def run(self):
        while self.loop():
            pass

    def loop(self) -> bool:
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
                self.state.key(event.key, True)
            if event.type == pygame.KEYUP:
                self.state.key(event.key, False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: work out why the position in the event does not match the
                #       position in the stored state if the mouse is clicked while it is
                #       moving
                self.state.mouse(event.button, event.pos, True)
            if event.type == pygame.MOUSEBUTTONUP:
                self.state.mouse(event.button, event.pos, False)
            if event.type == pygame.MOUSEMOTION:
                self.mouse.x = event.pos[0]
                self.mouse.y = event.pos[1]

        self.surface.fill(self.background_colour.colour_cache)
        view = self.view.value()
        if view is not None:
            render(view, self.surface, simplified=True)

        pygame.display.flip()
        return True
