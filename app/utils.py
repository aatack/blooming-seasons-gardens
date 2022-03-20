from typing import Tuple

from qt import (
    QAbstractAnimation,
    QColor,
    QFrame,
    QLayout,
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
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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

    def set_content_layout(self, new_layout):
        old_layout = self.content_area.layout()
        del old_layout

        self.content_area.setLayout(new_layout)

        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = new_layout.sizeHint().height()

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
