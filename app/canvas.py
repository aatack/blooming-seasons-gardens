from typing import Optional, Tuple

from qt import QColor, QFont, QFontMetrics, QPainter, QPen, QWidget


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self._painter: Optional[QPainter] = None

        self._font = QFont("segoeuisemibold", 24)
        self._font_metrics = QFontMetrics(self._font)

    def paintEvent(self, event):
        self._painter = QPainter(self)
        self._painter.setFont(self._font)

        self.set_colour((255, 0, 0))
        self.rectangle((200, 200), 150, 150)

        self.set_colour((0, 255, 0))
        self.circle((200, 200), 75)

        self.set_colour((0, 0, 255), width=10)
        self.line((200, 200), (350, 350))

        self.set_colour((0, 0, 0))
        self.text("Example text", (275, 275))

        self._painter = None

    def set_colour(self, colour: Tuple[int, int, int], width: Optional[int] = None):
        assert self._painter is not None
        colour = QColor(*colour)

        if width is not None:
            self._painter.setPen(QPen(colour, width))
        else:
            self._painter.setPen(colour)
        self._painter.setBrush(colour)

    def rectangle(self, position: Tuple[int, int], width: int, height: int):
        self._painter.fillRect(
            position[0], position[1], width, height, self._painter.brush()
        )

    def circle(self, position: Tuple[int, int], radius: int):
        self._painter.drawEllipse(position[0], position[1], 2 * radius, 2 * radius)

    def text(self, text: str, position: Tuple[int, int]):
        fudge_factor = 1.5  # Not sure exactly why this is needed but it seems to work
        self._painter.drawText(
            position[0],
            position[1] + (self._font_metrics.height() / fudge_factor),
            text,
        )

    def line(self, start: Tuple[int, int], end: Tuple[int, int]):
        self._painter.setRenderHint(QPainter.Antialiasing)
        self._painter.drawLine(*start, *end)
