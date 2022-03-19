import abc

from qt import QWidget

from app.camera import Camera, WidgetCamera


class Renderable:

    # TODO: add responses to events as they become needed

    @abc.abstractmethod
    def render(self, camera: Camera):
        """Render a visual representation using the given camera."""


class ExampleRenderable(Renderable):
    def render(self, camera: Camera):
        camera.rectangle((200.0, 200.0), 150.0, 150.0, (255, 0, 0))
        camera.circle((200.0, 200.0), 75.0, (0, 255, 0))
        camera.line((200.0, 200.0), (350.0, 350.0), 10.0, (0, 0, 255))
        camera.text((200.0, 200.0), "Example text", 75.0, (0, 0, 0))


class Canvas(QWidget):
    def __init__(self, renderable: Renderable):
        super().__init__()

        self._renderable = renderable

    def paintEvent(self, _):
        camera = WidgetCamera(self)

        self._renderable.render(camera)

        camera.destroy()
