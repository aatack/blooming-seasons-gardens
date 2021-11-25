from typing import Optional

import pygame

from components import Colour
from state import Derived, Keyboard, Mouse, Screen, State, Variable
from view import render, simplify

pygame.init()


class Window:
    def __init__(
        self,
        title: Optional[str] = None,
        background_colour: Colour = Colour(red=1.0, green=1.0, blue=1.0),
    ):
        pygame.init()

        self.screen = Screen(Variable(500), Variable(500))
        self.mouse = Mouse(Variable(0), Variable(0))
        self.keyboard = Keyboard()

        self.background_colour = background_colour

        self.title = title
        if self.title is not None:
            pygame.display.set_caption(self.title)

        self.surface = pygame.display.set_mode(
            tuple(self.screen.value()), pygame.RESIZABLE
        )

    def run(self, state: State):
        view = Derived(simplify, state.view())
        while self.loop(view):
            pass

    def loop(self, view: State) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.surface = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                self.screen.resize(event.w, event.h)
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                self.keyboard.key(event.key, True)
            if event.type == pygame.KEYUP:
                self.keyboard.key(event.key, False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: work out why the position in the event does not match the
                #       position in the stored state if the mouse is clicked while it is
                #       moving
                self.mouse.click(event.button, event.pos, True)
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse.click(event.button, event.pos, False)
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                self.mouse.x.modify(x)
                self.mouse.y.modify(y)

        self.surface.fill(self.background_colour.colour_cache)
        view_value = view.value()
        if view_value is not None:
            render(view_value, self.surface)

        pygame.display.flip()
        return True
