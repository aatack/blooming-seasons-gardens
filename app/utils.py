from typing import Tuple

from qt import QColor, QWidget


def set_widget_background(widget: QWidget, colour: Tuple[int, int, int]):
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    palette.setColor(widget.backgroundRole(), QColor(*colour))
    widget.setPalette(palette)
