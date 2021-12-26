from typing import Any, Optional

import pygame

from trickle.environment import Environment
from trickle.trickles.interaction import Keyboard, Mouse, Screen
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Derived, Variable
from trickle.visuals.visual import Visual

pygame.init()


class Window:
    def __init__(
        self, title: Optional[str] = None, background_colour: tuple = (1.0, 1.0, 1.0)
    ):
        pygame.init()

        self.environment = Environment(
            screen=Screen(Variable(500), Variable(500)),
            mouse=Mouse(Variable(0), Variable(0)),
            keyboard=Keyboard(),
        )

        self.background_colour = background_colour

        self.title = title
        if self.title is not None:
            pygame.display.set_caption(self.title)

        self.surface = pygame.display.set_mode(
            (
                int(self.environment.screen.width.value()),
                int(self.environment.screen.height.value()),
            ),
            pygame.RESIZABLE,
        )

    def run(self, view: Puddle):
        def simplify_view(v: Any) -> Visual:
            assert isinstance(v, Visual)
            return v.simplify()

        while self.loop(Derived(simplify_view, view)):
            pass

    def loop(self, view: Puddle) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.surface = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                self.environment.screen.resize(width=event.w, height=event.h)
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                self.environment.keyboard.key(event.key, True)
            if event.type == pygame.KEYUP:
                self.environment.keyboard.key(event.key, False)
            if event.type == pygame.MOUSEMOTION:
                # NOTE: responding to mouse motion events needs to happen before
                #       responding to mouse button events, otherwise their x and y
                #       coordinates do not match up
                x, y = event.pos

                self.environment.mouse.x.change(x)
                self.environment.mouse.y.change(y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                assert x == self.environment.mouse.x.value()
                assert y == self.environment.mouse.y.value()

                self.environment.mouse.click(event.button, True)
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos

                assert x == self.environment.mouse.x.value()
                assert y == self.environment.mouse.y.value()

                self.environment.mouse.click(event.button, False)

        self.surface.fill(tuple(int(colour * 255) for colour in self.background_colour))
        view.value().render(self.surface)

        pygame.display.flip()
        return True
