from typing import Tuple

from qt import QColor, QLayout, QSlider, Qt, QWidget


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
