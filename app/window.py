import time
from functools import cached_property
from typing import Optional

from qt import (
    QCoreApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QScrollArea,
    QStatusBar,
    Qt,
    QTimer,
    QWidget,
)
from settings import PLAN_VIEW_BACKGROUND

from app.camera import WidgetCamera
from app.canvas import Canvas, Renderable
from app.garden import Garden
from app.utils import set_widget_background


class Window(QMainWindow):
    def __init__(self, garden_path: str):
        super().__init__()

        self.garden_path = garden_path
        self.garden = Garden.read(self.garden_path)

        self.last_saved = time.time()
        self.update_last_saved_display()

        _ = self.plan_view

        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)

        self.garden.plan_view_widget = self.plan_view

        self.showMaximized()
        self.setWindowTitle(
            f"Blooming Seasons Design Studio - {garden_path.split('/')[-2]}"
        )

    def save(self):
        self.garden.write(self.garden_path)
        self.last_saved = time.time()
        self.update_last_saved_display()

    def new(self):
        path = QFileDialog.getExistingDirectory()

        raise NotImplementedError()

    def update_last_saved_display(self):
        elapsed = int((time.time() - self.last_saved) / 60)
        if elapsed == 0:
            string = "Last saved less than a minute ago"
        elif elapsed == 1:
            string = "Last saved 1 minute ago"
        else:
            string = f"Last saved {elapsed} minutes ago"
        self.last_saved_display.setText(string)

    @cached_property
    def menu_bar(self) -> QMenuBar:
        menu_bar = QMenuBar(self)

        file_menu = menu_bar.addMenu("&File")

        new_action = file_menu.addAction("New")
        new_action.triggered.connect(self.new)

        file_menu.addAction("Open")

        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save)

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(lambda: QCoreApplication.quit())

        return menu_bar

    @cached_property
    def central_widget(self) -> QWidget:
        central_widget = QWidget()

        views = QHBoxLayout()
        views.addWidget(self.editor_view, 1)
        views.addWidget(self.plan_view, 3)

        central_widget.setLayout(views)

        return central_widget

    @cached_property
    def status_bar(self) -> QStatusBar:
        status_bar = QStatusBar()

        status_bar.addWidget(self.last_saved_display)
        timer = QTimer(self)
        timer.timeout.connect(self.update_last_saved_display)
        timer.start(10000)

        return status_bar

    @cached_property
    def last_saved_display(self) -> QLabel:
        return QLabel("")

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
        plan_view = PlanView(self.garden.renderable)

        set_widget_background(plan_view, PLAN_VIEW_BACKGROUND)

        return plan_view


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
