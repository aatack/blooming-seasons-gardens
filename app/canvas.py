from typing import Optional, Tuple

from qt import QColor, QFont, QFontMetrics, QPainter, QPen, QWidget

from app.camera import WidgetCamera


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        camera = WidgetCamera(self)

        camera.rectangle((200.0, 200.0), 150.0, 150.0, (255, 0, 0))
        camera.circle((200.0, 200.0), 75.0, (0, 255, 0))
        camera.line((200.0, 200.0), (350.0, 350.0), 10.0, (0, 0, 255))
        camera.text((200.0, 200.0), "Example text", 75.0, (0, 0, 0))

        camera.destroy()
