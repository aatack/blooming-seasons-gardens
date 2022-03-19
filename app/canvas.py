import abc

from qt import QWidget

from app.camera import Camera, WidgetCamera


class Renderable:

    # TODO: add responses to events as they become needed

    @abc.abstractmethod
    def render(self, camera: Camera):
        """Render a visual representation using the given camera."""


class Canvas(QWidget):
    def __init__(self, renderable: Renderable):
        super().__init__()

        self._renderable = renderable

    def paintEvent(self, _):
        camera = WidgetCamera(self)

        self._renderable.render(camera)

        camera.destroy()
