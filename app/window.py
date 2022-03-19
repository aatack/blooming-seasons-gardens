from functools import cached_property
from typing import Optional

from qt import QHBoxLayout, QMainWindow, QMenuBar, QScrollArea, QStatusBar, Qt, QWidget

from app.camera import WidgetCamera
from app.canvas import Canvas, Renderable
from app.garden import Garden
from app.utils import set_widget_background


class Window(QMainWindow):
    def __init__(self, garden: Garden):
        super().__init__()

        self.garden = garden

        _ = self.plan_view

        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)

        self.garden.plan_view_widget = self.plan_view

    @cached_property
    def menu_bar(self) -> QMenuBar:
        menu_bar = QMenuBar(self)

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addAction("Exit")

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Cut")

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction("Help Content")
        help_menu.addAction("About")

        return menu_bar

    @cached_property
    def central_widget(self) -> QWidget:
        central_widget = QWidget()

        views = QHBoxLayout()
        views.addWidget(self.editor_view, 1)
        views.addWidget(self.plan_view, 2)

        central_widget.setLayout(views)

        return central_widget

    @cached_property
    def status_bar(self) -> QStatusBar:
        status_bar = QStatusBar()

        # TODO: add widgets and status information

        return status_bar

    @cached_property
    def editor_view(self) -> QWidget:
        scroll = QScrollArea()

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.garden.widget)

        return scroll

    @cached_property
    def plan_view(self) -> "PlanView":
        editor_view = PlanView(self.garden.renderable)

        set_widget_background(editor_view, (255, 255, 255))

        return editor_view


class PlanView(Canvas):
    def __init__(self, renderable: Renderable):
        super().__init__(renderable)

        self._camera_x = 1.0
        self._camera_y = 1.0

        self._camera_scale = 100.0

        self._mouse_x: Optional[int] = None
        self._mouse_y: Optional[int] = None

        self.setMouseTracking(True)

    def paintEvent(self, _):
        camera = WidgetCamera(self)

        self._renderable.render(
            camera.scale(self._camera_scale).shift(self._camera_x, self._camera_y)
        )

        camera.destroy()

    def mouseMoveEvent(self, event):
        if self._mouse_x is None:
            self._mouse_x = event.x()
        if self._mouse_y is None:
            self._mouse_y = event.y()

        if event.buttons() == Qt.LeftButton:
            x = event.x() - self._mouse_x
            y = event.y() - self._mouse_y

            self._camera_x += x / self._camera_scale
            self._camera_y += y / self._camera_scale

            self.update()

        self._mouse_x = event.x()
        self._mouse_y = event.y()

    def wheelEvent(self, event):
        change = event.angleDelta().y()

        # TODO: also calculate the new x and y coordinates

        if change != 0:
            fixed_x = (event.x() / self._camera_scale) - self._camera_x
            fixed_y = (event.y() / self._camera_scale) - self._camera_y
            zoom = 1.2 if change > 0 else (1 / 1.2)

            self._camera_x = ((fixed_x + self._camera_x) / zoom) - fixed_x
            self._camera_y = ((fixed_y + self._camera_y) / zoom) - fixed_y

            self._camera_scale *= zoom
            self.update()
