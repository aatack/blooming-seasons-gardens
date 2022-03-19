from functools import cached_property
from typing import List, Optional, Tuple

from qt import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSlider,
    Qt,
    QVBoxLayout,
    QWidget,
)

from app.utils import build_colour_slider


class Garden:
    def __init__(self):
        self._beds: List["Bed"] = []

    def add_bed(self, bed: "Bed"):
        bed.set_garden(self)
        self._beds.append(bed)

        self._beds_layout.addWidget(bed.widget)

    def remove_bed(self, bed: "Bed"):
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

        dump = QPushButton("Dump")
        dump.clicked.connect(lambda: print(self.serialise()))

        add_bed = QPushButton("Add Bed")
        add_bed.clicked.connect(add_new_bed)

        layout.addWidget(dump)
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

        self._plants_layout.addWidget(plant.widget)

    def remove_plant(self, plant: "Plant"):
        self._plants.remove(plant)
        self._plants_layout.removeWidget(plant.widget)

        plant.remove()

    def remove(self):
        self._garden = None
        self.widget.deleteLater()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        set_name = QLineEdit()
        set_name.textEdited.connect(lambda: self.set_name(set_name.text()))

        def add_new_plant():
            self.add_plant(Plant())

        add_plant = QPushButton("Add Plant")
        add_plant.clicked.connect(add_new_plant)

        remove = QPushButton("Remove")
        remove.clicked.connect(lambda: self._garden.remove_bed(self))

        layout.addWidget(set_name)
        layout.addWidget(add_plant)
        layout.addLayout(self._plants_layout)
        layout.addWidget(remove)

        return widget

    @cached_property
    def _plants_layout(self) -> QVBoxLayout:
        return QVBoxLayout()

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

        self._name = ""
        self._size = 0.1
        self._colour = (0, 64, 128)

    def set_bed(self, bed: Bed):
        assert isinstance(bed, Bed)
        assert self._bed is None

        self._bed = bed

    def set_name(self, name: str):
        self._name = name

    def set_size(self, size: float):
        self._size = size

    def set_colour(self, colour: Tuple[int, int, int]):
        self._colour = colour

    def remove(self):
        self._garden = None
        self.widget.deleteLater()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

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

        remove = QPushButton("Remove")
        remove.clicked.connect(lambda: self._bed.remove_plant(self))

        layout.addLayout(self._form)
        layout.addWidget(remove)

        widget.setLayout(layout)
        return widget

    @cached_property
    def _form(self) -> QFormLayout:
        form = QFormLayout()

        # Name
        name_label = QLabel("Name:")
        name_edit = QLineEdit()
        name_edit.textEdited.connect(lambda: self.set_name(name_edit.text()))
        form.addRow(name_label, name_edit)

        # Size
        size_label = QLabel("Size:")
        size_edit = QLineEdit()

        def update_size():
            try:
                size = float(size_edit.text())
                self.set_size(size)
            except ValueError:
                pass

        size_edit.textEdited.connect(update_size)
        form.addRow(size_label, size_edit)

        # Colour
        colour_label = QLabel("Colour:")
        colour_layout = QHBoxLayout()

        red = build_colour_slider("red", colour_layout, self._colour[0])
        green = build_colour_slider("green", colour_layout, self._colour[1])
        blue = build_colour_slider("blue", colour_layout, self._colour[2])

        def update_colour():
            self.set_colour((red.value(), green.value(), blue.value()))

        red.valueChanged.connect(update_colour)
        green.valueChanged.connect(update_colour)
        blue.valueChanged.connect(update_colour)

        form.addRow(colour_label, colour_layout)

        return form

    def serialise(self) -> dict:
        return {
            "name": self._name,
            "size": self._size,
            "colour": list(self._colour)
        }

    @staticmethod
    def deserialise(json: dict) -> "Plant":
        plant = Plant()

        plant.set_name(json["name"])
        plant.set_size(json["size"])
        plant.set_colour(tuple(json["colour"]))

        return plant
