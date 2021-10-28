from state import *
import pygame


@struct
class Colour:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    def render(self, surface: pygame.Surface):
        surface.fill((int(self.red * 255), int(self.green * 255), int(self.blue * 255)))


@struct
class Point:
    x: float = 0.0
    y: float = 0.0
