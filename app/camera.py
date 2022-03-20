import abc
from typing import Optional, Tuple

from qt import QColor, QFont, QFontMetrics, QPainter, QPen, QPixmap, QWidget

Point = Tuple[float, float]
Colour = Tuple[int, int, int]


class Camera:
    @abc.abstractmethod
    def transform(self, point: Point) -> Point:
        pass

    @abc.abstractmethod
    def inverse_transform(self, point: Point) -> Point:
        pass

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

    @abc.abstractmethod
    def image(self, position: Point, height: float, image: QPixmap):
        pass

    def scale(self, scale: float) -> "Camera":
        return ScaledCamera(self, scale)

    def shift(self, x: float = 0.0, y: float = 0.0) -> "Camera":
        return ShiftedCamera(self, (x, y))


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

    def transform(self, point: Point) -> Point:
        return point

    def inverse_transform(self, point: Point) -> Point:
        return point

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

    def image(self, position: Point, height: float, image: QPixmap):
        width = image.width() * (height / image.height())
        self._painter.drawPixmap(
            int(position[0]), int(position[1]), int(width), int(height), image
        )


class ScaledCamera(Camera):
    def __init__(self, camera: Camera, scale: float):
        self._camera = camera
        self._scale = scale

    def transform(self, point: Point) -> Point:
        return point[0] * self._scale, point[1] * self._scale

    def inverse_transform(self, point: Point) -> Point:
        return point[0] / self._scale, point[1] / self._scale

    def rectangle(self, position: Point, width: float, height: float, colour: Colour):
        self._camera.rectangle(
            self.transform(position), width * self._scale, height * self._scale, colour
        )

    def circle(self, position: Point, radius: float, colour: Colour):
        self._camera.circle(self.transform(position), radius * self._scale, colour)

    def line(self, start: Point, end: Point, width: float, colour: Colour):
        self._camera.line(
            self.transform(start), self.transform(end), width * self._scale, colour
        )

    def text(self, position: Point, text: str, height: float, colour: Colour):
        self._camera.text(self.transform(position), text, height * self._scale, colour)

    def image(self, position: Point, height: float, image: QPixmap):
        self._camera.image(self.transform(position), height * self._scale, image)


class ShiftedCamera(Camera):
    def __init__(self, camera: Camera, shift: Tuple[float, float]):
        self._camera = camera
        self._shift = shift

    def transform(self, point: Point) -> Point:
        return point[0] + self._shift[0], point[1] + self._shift[1]

    def inverse_transform(self, point: Point) -> Point:
        return point[0] - self._shift[0], point[1] - self._shift[1]

    def rectangle(self, position: Point, width: float, height: float, colour: Colour):
        self._camera.rectangle(self.transform(position), width, height, colour)

    def circle(self, position: Point, radius: float, colour: Colour):
        self._camera.circle(self.transform(position), radius, colour)

    def line(self, start: Point, end: Point, width: float, colour: Colour):
        self._camera.line(self.transform(start), self.transform(end), width, colour)

    def text(self, position: Point, text: str, height: float, colour: Colour):
        self._camera.text(self.transform(position), text, height, colour)

    def image(self, position: Point, height: float, image: QPixmap):
        self._camera.image(self.transform(position), height, image)
