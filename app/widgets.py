from functools import cached_property
from typing import Any, Callable, Optional

from qt import (
    QColor,
    QCursor,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPainter,
    QPointF,
    QPushButton,
    Qt,
    QVBoxLayout,
    QWidget,
)
from settings import (
    COLLAPSIBLE_BODY_BACKGROUND,
    COLLAPSIBLE_HEADER_BACKGROUND,
    HIGHLIGHT_BACKGROUND,
)

from app.utils import set_widget_background


class Collapsible(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._title = ""
        self._collapsed = True

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

    @collapsed.setter
    def collapsed(self, collapsed: bool):
        self._collapsed = collapsed

        self._body.setVisible(not self.collapsed)
        self._arrow.down = not self.collapsed

    @cached_property
    def _layout(self) -> QLayout:
        layout = QVBoxLayout()

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._header)
        layout.addWidget(self._body)

        return layout

    class Header(QFrame):
        def __init__(
            self,
            arrow: "Arrow",
            label: QLabel,
            callback: Callable[[], None],
            parent: Optional[QWidget] = None,
        ):
            super().__init__(parent)

            self._callback = callback

            self.setMinimumHeight(24)
            self.setMaximumHeight(24)

            layout = QHBoxLayout()
            self.setLayout(layout)

            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            layout.addWidget(arrow)
            layout.addWidget(label)

            set_widget_background(self, COLLAPSIBLE_HEADER_BACKGROUND)

            self.setMouseTracking(True)

        def mousePressEvent(self, event):
            self._callback()

        def enterEvent(self, event):
            set_widget_background(self, HIGHLIGHT_BACKGROUND)

        def leaveEvent(self, event):
            set_widget_background(self, COLLAPSIBLE_HEADER_BACKGROUND)

    @cached_property
    def _header(self) -> QFrame:
        def callback():
            self.collapsed = not self.collapsed

        return self.Header(self._arrow, self._label, callback)

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
        set_widget_background(body, COLLAPSIBLE_BODY_BACKGROUND)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(body)
        self.body.setLayout(layout)

    @cached_property
    def _body(self) -> QWidget:
        body = QWidget()

        body.setVisible(not self.collapsed)
        self._arrow.down = not self.collapsed

        return body


class Arrow(QFrame):

    DOWN = (
        QPointF(7.0, 8.0),
        QPointF(17.0, 8.0),
        QPointF(12.0, 18.0),
    )

    RIGHT = (
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


class DragButton(QPushButton):
    def __init__(
        self,
        text: str,
        move_callback: Optional[Callable[[int, int], None]] = None,
        scroll_callback: Optional[Callable[[bool], None]] = None,
    ):
        super().__init__(text)

        self._move_callback = move_callback
        self._scroll_callback = scroll_callback

        self._initial_x: Optional[int] = None
        self._initial_y: Optional[int] = None

        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self._initial_x, self._initial_y = QCursor.pos().x(), QCursor.pos().y()
        self.setCursor(Qt.BlankCursor)

    def mouseReleaseEvent(self, event):
        self._initial_x, self._initial_y = None, None
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if self._initial_x is None or self._initial_y is None:
            return

        if event.buttons() == Qt.LeftButton:
            dx = QCursor.pos().x() - self._initial_x
            dy = QCursor.pos().y() - self._initial_y

            QCursor.setPos(self._initial_x, self._initial_y)

            if self._move_callback is not None:
                self._move_callback(dx, dy)

    def wheelEvent(self, event):
        if self._initial_x is None or self._initial_y is None:
            return

        if self._scroll_callback is not None:
            up = event.angleDelta().y() > 0
            self._scroll_callback(up)
