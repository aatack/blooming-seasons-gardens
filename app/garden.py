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

    def add_bed(self, bed: "Bed"):
        bed.set_garden(self)
        self._beds.append(bed)

        self._beds_layout.addWidget(bed.widget)

    def remove_bed(self, bed: "Bed"):
        print(bed.serialise())
        self._beds.remove(bed)
        self._beds_layout.removeWidget(bed.widget)

        bed.remove()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        def add_new_bed():
            self.add_bed(Bed())

        add_bed = QPushButton("Add Bed")
        add_bed.clicked.connect(add_new_bed)

        layout.addWidget(add_bed)
        layout.addLayout(self._beds_layout)
        layout.addStretch()

        return widget

    @cached_property
    def _beds_layout(self) -> QVBoxLayout:
        return QVBoxLayout()

    def serialise(self) -> list:
        return [bed.serialise() for bed in self._beds]

    @staticmethod
    def deserialise(json: list) -> "Garden":
        garden = Garden()
        
        for bed in json:
            garden.add_bed(Bed.deserialise(bed))

        return garden


class Bed:
    def __init__(self):
        self._garden: Optional[Garden] = None

        self._name = ""
        self._plants: List["Plant"] = []

    def set_garden(self, garden: Garden):
        assert isinstance(garden, Garden)
        assert self._garden is None

        self._garden = garden

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def add_plant(self, plant: "Plant"):
        plant.set_bed(self)
        self._plants.append(plant)

    def remove(self):
        self.widget.deleteLater()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        set_name = QLineEdit()
        set_name.textEdited.connect(lambda: self.set_name(set_name.text()))

        remove = QPushButton("Remove")
        remove.clicked.connect(lambda: self._garden.remove_bed(self))

        layout.addWidget(set_name)
        layout.addWidget(remove)

        return widget

    def serialise(self) -> dict:
        return {
            "name": self._name,
            "plants": [plant.serialise() for plant in self._plants]
        }

    @staticmethod
    def deserialise(json: dict) -> "Bed":
        bed = Bed()

        for plant in json["plants"]:
            bed.add_plant(Plant.deserialise(plant))

        return bed


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

    def serialise(self) -> dict:
        return {}

    @staticmethod
    def deserialise(json: dict) -> "Plant":
        return Plant()
