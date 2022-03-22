from qt import QColor, QFrame, QPainter, QPointF, QWidget


class Arrow(QFrame):

    RIGHT = (
        QPointF(7.0, 8.0),
        QPointF(17.0, 8.0),
        QPointF(12.0, 18.0),
    )

    DOWN = (
        QPointF(8.0, 7.0),
        QPointF(18.0, 12.0),
        QPointF(8.0, 17.0),
    )

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setMaximumSize(24, 24)

        self._down = False
        self._arrow = self.RIGHT

    @property
    def down(self) -> bool:
        return self._down

    @down.setter
    def down(self, down: bool):
        if down:
            self._arrow = self.DOWN
        else:
            self._arrow = self.RIGHT
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(QColor(192, 192, 192))
        painter.setPen(QColor(64, 64, 64))
        painter.drawPolygon(*self._arrow)

        painter.end()
