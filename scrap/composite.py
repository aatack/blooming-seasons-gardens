from scrap.base import Scrap
import wrapper.renderable as renderable
from typing import List


class Void(Scrap):
    pass


class Group(Scrap):
    def __init__(self, *children: List[Scrap]):
        self.children = children

    def cache(self) -> renderable.Renderable:
        return renderable.Group(self.children)
