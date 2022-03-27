from functools import cached_property

from qt import QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget

from app.utils import create_new_garden, open_existing_garden


class Splash(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(self.central_widget)

        self.resize(400, 200)
        self.setWindowTitle("Blooming Seasons Design Studio")

        self.show()

    @cached_property
    def central_widget(self) -> QWidget:
        widget = QWidget()
        outer_layout = QHBoxLayout()
        inner_layout = QVBoxLayout()
        widget.setLayout(outer_layout)

        outer_layout.addStretch()
        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch()

        inner_layout.setSpacing(10)
        inner_layout.addStretch()

        new_button = QPushButton("Create new garden")
        new_button.setMinimumWidth(150)
        new_button.clicked.connect(create_new_garden)
        inner_layout.addWidget(new_button)

        open_button = QPushButton("Open existing garden")
        open_button.setMinimumWidth(150)
        open_button.clicked.connect(open_existing_garden)
        inner_layout.addWidget(open_button)

        inner_layout.addStretch()

        return widget
