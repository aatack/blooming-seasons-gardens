from functools import cached_property

from qt import *

from app.canvas import Canvas
from app.garden import Garden
from app.utils import set_widget_background


class Window(QMainWindow):
    def __init__(self, garden: Garden):
        super().__init__()

        self.garden = garden

        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)

    @cached_property
    def status_bar(self) -> QStatusBar:
        status_bar = QStatusBar()

        # TODO: add widgets and status information

        return status_bar

    @cached_property
    def central_widget(self) -> QWidget:
        central_widget = QWidget()

        views = QHBoxLayout()
        views.addWidget(self.editor_view, 1)
        views.addWidget(self.plan_view, 2)

        central_widget.setLayout(views)

        return central_widget

    @cached_property
    def editor_view(self) -> QWidget:
        scroll = QScrollArea()

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.garden.widget)

        return scroll

    @cached_property
    def plan_view(self) -> QWidget:
        editor_view = Canvas(self.garden.renderable)

        set_widget_background(editor_view, (255, 255, 255))

        return editor_view
