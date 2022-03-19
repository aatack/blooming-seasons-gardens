from typing import List, Optional


class Garden:
    def __init__(self):
        self._beds: List["Bed"] = []


class Bed:
    def __init__(self):
        self._garden: Optional[Garden] = None

        self._plants: List["Plant"] = []

    def set_garden(self, garden: Garden):
        assert isinstance(garden, Garden)
        assert self._garden is None

        self._bed


class Plant:
    def __init__(self):
        self._bed: Optional[Bed] = None

    def set_bed(self, bed: Bed):
        assert isinstance(bed, Bed)
        assert self._bed is None

        self._bed = bed
