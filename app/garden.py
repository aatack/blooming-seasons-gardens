from functools import cached_property
from typing import List, Optional

from qt import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class Garden:
    def __init__(self):
        self._beds: List["Bed"] = []

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        add_bed = QPushButton("Add Bed")
        layout.addWidget(add_bed)
        layout.addStretch()

        return widget


class Bed:
    def __init__(self):
        self._garden: Optional[Garden] = None

        self._plants: List["Plant"] = []

    def set_garden(self, garden: Garden):
        assert isinstance(garden, Garden)
        assert self._garden is None

        self._bed


class Plant:
    def __init__(self):
        self._bed: Optional[Bed] = None

    def set_bed(self, bed: Bed):
        assert isinstance(bed, Bed)
        assert self._bed is None

        self._bed = bed

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()

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

        widget.setLayout(example_form)
        return widget
