from typing import Tuple

from qt import (
    QAbstractAnimation,
    QColor,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPainter,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QScrollArea,
    QSizePolicy,
    QSlider,
    Qt,
    QToolButton,
    QVBoxLayout,
    QWidget,
    pyqtSlot,
)


def set_widget_background(widget: QWidget, colour: Tuple[int, int, int]):
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    palette.setColor(widget.backgroundRole(), QColor(*colour))
    widget.setPalette(palette)


def build_colour_slider(colour: str, parent: QLayout, initial_value: int) -> QSlider:
    slider = QSlider(Qt.Horizontal)
    parent.addWidget(slider)

    slider.setStyleSheet(
        "QSlider::handle:horizontal {background-color: " + colour + "}"
    )

    slider.setMinimum(0)
    slider.setMaximum(255)
    slider.setSingleStep(1)
    slider.setValue(initial_value)

    return slider


class Collapsible(QWidget):
    def __init__(self, title: str = ""):
        super().__init__()

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_area.setFrameShape(QFrame.NoFrame)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward if not checked else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def set_content_layout(self, new_layout: QLayout):
        old_layout = self.content_area.layout()
        del old_layout

        self.content_area.setLayout(new_layout)
        self.update_animation_height()

    def update_animation_height(self):
        collapsed_height = (
            self.toggle_button.sizeHint().height()  # - self.content_area.maximumHeight()
        )
        content_height = self.content_area.layout().sizeHint().height()
        print("Updating animation height", collapsed_height, content_height)

        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(100)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )

        content_animation.setDuration(100)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


__author__ = "Caroline Beyne"

from PyQt5 import QtCore, QtGui


class FrameLayout(QWidget):
    def __init__(self, parent=None, title=None):
        QFrame.__init__(self, parent=parent)

        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QVBoxLayout(self)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collasped))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped))

        self.initCollapsable()

    def initTitleFrame(self, title, collapsed):
        self._title_frame = self.TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QWidget()
        self._content_layout = QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        self._title_frame.set_callback(self.toggleCollapsed)
        # QtCore.QObject.connect(
        #     self._title_frame, QtCore.SIGNAL("clicked()"), self.toggleCollapsed
        # )

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

    ############################
    #           TITLE          #
    ############################
    class TitleFrame(QFrame):
        def __init__(self, parent=None, title="", collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMinimumHeight(24)
            self.move(QtCore.QPoint(24, 0))
            self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow = None
            self._title = None

            self._hlayout.addWidget(self.initArrow(collapsed))
            self._hlayout.addWidget(self.initTitle(title))

            self._callback = None

        def set_callback(self, callback):
            self._callback = callback

        def initArrow(self, collapsed):
            self._arrow = FrameLayout.Arrow(collapsed=collapsed)
            self._arrow.setStyleSheet("border:0px")

            return self._arrow

        def initTitle(self, title=None):
            self._title = QLabel(title)
            self._title.setMinimumHeight(24)
            self._title.move(QtCore.QPoint(24, 0))
            self._title.setStyleSheet("border:0px")

            return self._title

        def mousePressEvent(self, event):
            # self.emit(QtCore.SIGNAL("clicked()"))
            if self._callback is not None:
                self._callback()

            return super(FrameLayout.TitleFrame, self).mousePressEvent(event)

    #############################
    #           ARROW           #
    #############################
    class Arrow(QFrame):
        def __init__(self, parent=None, collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (
                QtCore.QPointF(7.0, 8.0),
                QtCore.QPointF(17.0, 8.0),
                QtCore.QPointF(12.0, 18.0),
            )
            # vertical == 1
            self._arrow_vertical = (
                QtCore.QPointF(8.0, 7.0),
                QtCore.QPointF(18.0, 12.0),
                QtCore.QPointF(8.0, 17.0),
            )
            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal

        def paintEvent(self, event):
            painter = QPainter()
            painter.begin(self)
            painter.setBrush(QColor(192, 192, 192))
            painter.setPen(QColor(64, 64, 64))
            painter.drawPolygon(*self._arrow)
            painter.end()
