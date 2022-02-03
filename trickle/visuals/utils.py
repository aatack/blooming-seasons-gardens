from typing import Optional

import pygame
from trickle.visuals.visual import Visual


def debug_visual(
    visual: Visual, width: Optional[int] = None, height: Optional[int] = None
):
    if width is None:
        width = int(visual.right() + 100)
    if height is None:
        height = int(visual.bottom() + 100)

    surface = pygame.display.set_mode((width, height,), pygame.RESIZABLE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.QUIT:
                return

        surface.fill((255,) * 3)
        visual.render(surface)
        pygame.display.flip()
