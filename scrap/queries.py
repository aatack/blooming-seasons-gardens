from scrap.base import Scrap
from scrap.data import Point


class Contains(Scrap):
    def __init__(self, point: Point):
        self.point = point
