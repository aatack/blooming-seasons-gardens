from functools import cached_property

from qt import *

from app.utils import set_widget_background


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

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
        views.addWidget(self.plan_view, 1)
        views.addWidget(self.editor_view, 2)

        central_widget.setLayout(views)

        return central_widget

    @cached_property
    def plan_view(self) -> QWidget:
        plan_view = QWidget()

        plan_view.setLayout(self.example_form)
        
        return plan_view

    @cached_property
    def editor_view(self) -> QWidget:
        editor_view = QWidget()

        set_widget_background(editor_view, (255, 255, 255))

        return editor_view

    @cached_property
    def example_form(self) -> QFormLayout:
        example_form = QFormLayout()

        name_label = QLabel("Name")
        name_edit = QLineEdit()

        address_label = QLabel("Address")
        first_address_edit = QLineEdit()
        second_address_edit = QLineEdit()
        example_form.addRow(name_label, name_edit)
        vertical = QVBoxLayout()

        vertical.addWidget(first_address_edit)
        vertical.addWidget(second_address_edit)
        example_form.addRow(address_label, vertical)
        horizontal = QHBoxLayout()

        male_button = QRadioButton("Male")
        female_button = QRadioButton("Female")
        horizontal.addWidget(male_button)
        horizontal.addWidget(female_button)
        horizontal.addStretch()

        example_form.addRow(QLabel("sex"), horizontal)
        submit = QPushButton("Submit")
        example_form.addRow(submit, QPushButton("Cancel"))
        submit.clicked.connect(lambda: self.status_bar.showMessage("Submitted", 500))

        return example_form
