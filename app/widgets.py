from functools import cached_property
from typing import Optional

from qt import (
    QColor,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPainter,
    QPointF,
    QVBoxLayout,
    QWidget,
)


class Collapsible(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._title = ""
        self._collapsed = False

        self.setLayout(self._layout)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title
        self._label.setText(self.title)

    @property
    def collapsed(self) -> bool:
        return self._collapsed

    @cached_property
    def _layout(self) -> QLayout:
        layout = QVBoxLayout()

        layout.addWidget(self._header)
        layout.addWidget(self._body)

        return layout

    @cached_property
    def _header(self) -> QFrame:
        header = QFrame(self)

        header.setMinimumHeight(24)
        header.setMaximumHeight(24)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._arrow)
        layout.addWidget(self._label)

        return header

    @cached_property
    def _arrow(self) -> QWidget:
        return Arrow()

    @cached_property
    def _label(self) -> QLabel:
        label = QLabel()
        label.setText(self.title)
        return label

    @property
    def body(self) -> QWidget:
        return self._body

    @body.setter
    def body(self, body: QWidget):
        layout = QVBoxLayout()
        layout.addWidget(body)
        self.body.setLayout(layout)

    @cached_property
    def _body(self) -> QWidget:
        body = QWidget()
        body.setVisible(not self.collapsed)
        return body


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

    def __init__(self, parent: Optional[QWidget] = None):
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
