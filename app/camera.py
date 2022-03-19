import abc
from typing import Optional, Tuple

from qt import QColor, QFont, QFontMetrics, QPainter, QPen, QWidget

Point = Tuple[float, float]
Colour = Tuple[int, int, int]


class Camera:
    @abc.abstractmethod
    def rectangle(self, position: Point, width: float, height: float, colour: Colour):
        pass

    @abc.abstractmethod
    def circle(self, position: Point, radius: float, colour: Colour):
        pass

    @abc.abstractmethod
    def line(self, start: Point, end: Point, width: float, colour: Colour):
        pass

    @abc.abstractmethod
    def text(self, position: Point, text: str, height: float, colour: Colour):
        pass


class WidgetCamera(Camera):
    def __init__(self, widget: QWidget):
        self._painter: Optional[QPainter] = QPainter(widget)

        # Not sure exactly why this is needed but it seems to work
        self._fudge_factor = 1.5

        self._base_font_size = 24
        self._base_font_family = "segoeuisemibold"

        self._font = QFont(self._base_font_family, self._base_font_size)
        self._font_metrics = QFontMetrics(self._font)

        self._font_height = self._font_metrics.height() / self._fudge_factor

    def destroy(self):
        self._painter = None

    def set_colour(self, colour: Tuple[int, int, int], width: Optional[int] = None):
        assert self._painter is not None
        colour = QColor(*colour)

        if width is not None:
            self._painter.setPen(QPen(colour, width))
        else:
            self._painter.setPen(colour)
        self._painter.setBrush(colour)

    def rectangle(self, position: Point, width: float, height: float, colour: Colour):
        self.set_colour(colour)
        self._painter.fillRect(
            int(position[0]),
            int(position[1]),
            int(width),
            int(height),
            self._painter.brush(),
        )

    def circle(self, position: Point, radius: float, colour: Colour):
        self.set_colour(colour)
        self._painter.drawEllipse(
            int(position[0]), int(position[1]), int(2 * radius), int(2 * radius)
        )

    def line(self, start: Point, end: Point, width: float, colour: Colour):
        self.set_colour(colour, width=width)
        self._painter.setRenderHint(QPainter.Antialiasing)
        self._painter.drawLine(*map(int, start + end))

    def text(self, position: Point, text: str, height: float, colour: Colour):
        self.set_colour(colour)

        height_factor = height / self._font_height
        font_size = int(self._base_font_size * height_factor)

        self._painter.setFont(QFont(self._base_font_family, font_size))

        self._painter.drawText(int(position[0]), int(position[1] + height), text)
