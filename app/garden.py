from functools import cached_property
from os.path import isfile
from typing import Iterator, List, Optional, Tuple

from qt import (
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPixmap,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.camera import Camera
from app.canvas import Renderable
from app.utils import build_colour_slider
from app.widgets import Collapsible


class Garden:
    class Renderable(Renderable):
        def __init__(self, garden: "Garden"):
            super().__init__()

            self.garden = garden

        def render(self, camera: Camera):
            self.garden.background.renderable.render(camera)

            for bed in self.garden.beds:
                bed.renderable.render(camera)

    def __init__(self):
        self._background: Background = Background(self)
        self._beds: List["Bed"] = []

        self.plan_view_widget: Optional[QWidget] = None
        self._rendered = False

    def update_render(self):
        if self._rendered:
            assert self.plan_view_widget is not None
            self.plan_view_widget.update()

    @property
    def background(self) -> "Background":
        return self._background

    @property
    def beds(self) -> Iterator["Bed"]:
        yield from self._beds

    def add_bed(self, bed: "Bed"):
        bed.garden = self
        self._beds.append(bed)

        self._beds_layout.addWidget(bed.widget)
        self.update_render()

    def remove_bed(self, bed: "Bed"):
        self._beds.remove(bed)
        self._beds_layout.removeWidget(bed.widget)

        bed.remove()
        self.update_render()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addWidget(self.background.widget)

        def add_new_bed():
            self.add_bed(Bed())

        debug = QPushButton("Debug")
        debug.clicked.connect(lambda: print(self.serialise()))

        add_bed = QPushButton("Add Bed")
        add_bed.clicked.connect(add_new_bed)

        layout.addWidget(debug)
        layout.addWidget(add_bed)
        layout.addLayout(self._beds_layout)
        layout.addStretch()

        return widget

    @cached_property
    def _beds_layout(self) -> QVBoxLayout:
        return QVBoxLayout()

    @cached_property
    def renderable(self) -> Renderable:
        self._rendered = True
        return Garden.Renderable(self)

    def serialise(self) -> list:
        return {
            "background": self.background.serialise(),
            "beds": [bed.serialise() for bed in self.beds],
        }

    @staticmethod
    def deserialise(json: list) -> "Garden":
        garden = Garden()

        garden.background.deserialise(json["background"])

        for bed in json["beds"]:
            garden.add_bed(Bed.deserialise(bed))

        return garden

    def write(self, path: str):
        import json

        with open(path + "garden.bsg", "w") as file:
            json.dump(self.serialise(), file)

    @staticmethod
    def read(path: str) -> "Garden":
        import json

        with open(path + "garden.bsg", "r") as file:
            garden = Garden.deserialise(json.load(file))

        if isfile(background := path + "background.png"):
            garden.background.path = background

        return garden


class Background:
    class Renderable(Renderable):
        def __init__(self, background: "Background"):
            self.background = background

        def render(self, camera: Camera):
            if (image := self.background.image) is not None:
                camera.image(self.background.position, self.background.height, image)

    def __init__(self, garden: Garden):
        self._garden = garden

        self._position = (0.0, 0.0)
        self._height = 10.0
        self._path: Optional[str] = None
        self._image: Optional[QPixmap] = None

        self._rendered = False

    def update_render(self):
        if self._rendered:
            self.garden.update_render()

    @property
    def garden(self) -> Garden:
        return self._garden

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, position: Tuple[float, float]):
        self._position = position
        self.update_render()

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, height: float):
        self._height = height
        self.update_render()

    @property
    def path(self) -> Optional[str]:
        return self._path

    @path.setter
    def path(self, path: Optional[str]):
        self._path = path
        if path is None:
            self._image = None
        else:
            self._image = QPixmap(path)
            assert self.image.height() > 0 and self.image.width() > 0
        self.update_render()

    @property
    def image(self) -> Optional[QPixmap]:
        return self._image

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        form = QFormLayout()
        widget.setLayout(form)

        # Height
        height_label = QLabel("Background height:")
        height_edit = QLineEdit(str(self.height))

        def update_height():
            try:
                height = float(height_edit.text())
                self.height = height
            except ValueError:
                pass

        height_edit.textEdited.connect(update_height)
        form.addRow(height_label, height_edit)

        # Position
        position_label = QLabel("Background position:")
        position_layout = QHBoxLayout()

        x_label = QLabel("x =")
        x_edit = QLineEdit(str(self.position[0]))
        y_label = QLabel("y =")
        y_edit = QLineEdit(str(self.position[1]))

        position_layout.addWidget(x_label)
        position_layout.addWidget(x_edit)
        position_layout.addWidget(y_label)
        position_layout.addWidget(y_edit)

        def update_position():
            try:
                x, y = float(x_edit.text()), float(y_edit.text())
                self.position = (x, y)
            except ValueError:
                pass

        x_edit.textEdited.connect(update_position)
        y_edit.textEdited.connect(update_position)

        form.addRow(position_label, position_layout)

        # Image
        def choose_image():
            path, _ = QFileDialog.getOpenFileName()
            if len(path) != 0:  # If user did not cancel the selection
                image = QPixmap(path)
                if image.size().width() == 0 and image.size().height() == 0:
                    # User selected a non-image file
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setText("Could not load background")
                    error.setInformativeText(
                        "Tried to load a file that is not a valid background.  "
                        "This is likely because it is not an image file."
                    )
                    error.setWindowTitle("Error")
                    error.exec()
                else:
                    # NOTE: currently this will lead to the change in background being
                    #       saved immediately, even if the user did not request it
                    # TODO: fix the above note

                    from app.run import RuntimeEnvironment
                    from app.window import Window

                    window = RuntimeEnvironment.window
                    assert isinstance(window, Window)
                    path = window.path + "background.png"
                    image.save(path)
                    # Bit of a workaround - should probably just have a `refresh`
                    # function
                    self.path = path

        choose_image_button = QPushButton("Choose new background")
        choose_image_button.clicked.connect(choose_image)
        form.addWidget(choose_image_button)

        return widget

    @cached_property
    def renderable(self) -> Renderable:
        self._rendered = True
        return Background.Renderable(self)

    def serialise(self) -> dict:
        # TODO: work out how best to also save the image to disk
        return {"height": self._height, "position": list(self._position)}

    def deserialise(self, json: dict):
        self.height = json["height"]
        self.position = tuple(json["position"])


class Bed:
    class Renderable(Renderable):
        def __init__(self, bed: "Bed"):
            super().__init__()

            self.bed = bed

        def render(self, camera: Camera):
            bed_camera = camera.shift(*self.bed.position)
            for plant in self.bed.plants:
                plant.renderable.render(bed_camera)
            for label in self.bed.labels:
                label.renderable.render(bed_camera)
            for arrow in self.bed.arrows:
                arrow.renderable.render(bed_camera)

    def __init__(self):
        self._garden: Optional[Garden] = None

        self._name = ""
        self._position = (0.0, 0.0)
        self._plants: List["Plant"] = []
        self._labels: List["Label"] = []
        self._arrows: List["Arrow"] = []

        self._rendered = False

    def update_render(self):
        if self._rendered:
            self.garden.update_render()

    @property
    def garden(self) -> Garden:
        assert self._garden is not None
        return self._garden

    @garden.setter
    def garden(self, garden: Garden):
        assert isinstance(garden, Garden)
        assert self._garden is None

        self._garden = garden

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self._collapsible.title = self.name
        self.update_render()

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, position: Tuple[float, float]):
        self._position = position
        self.update_render()

    @property
    def plants(self) -> Iterator["Plant"]:
        yield from self._plants

    def add_plant(self, plant: "Plant"):
        plant.bed = self
        self._plants.append(plant)

        self._plants_layout.addWidget(plant.widget)
        self.update_render()

    def remove_plant(self, plant: "Plant"):
        self._plants.remove(plant)
        self._plants_layout.removeWidget(plant.widget)

        plant.remove()
        self.update_render()

    @property
    def labels(self) -> Iterator["Label"]:
        yield from self._labels

    def add_label(self, label: "Label"):
        label.bed = self
        self._labels.append(label)

        # TODO: do we need a specialised labels layout?
        self._plants_layout.addWidget(label.widget)
        self.update_render()

    def remove_label(self, label: "Label"):
        self._labels.remove(label)
        # TODO: do we need a specialised labels layout?
        self._plants_layout.removeWidget(label.widget)

        label.remove()
        self.update_render()

    @property
    def arrows(self) -> Iterator["Arrow"]:
        yield from self._arrows

    def add_arrow(self, arrow: "Arrow"):
        arrow.bed = self
        self._arrows.append(arrow)

        # TODO: do we need a specialised arrows layout?
        self._plants_layout.addWidget(arrow.widget)
        self.update_render()

    def remove_arrow(self, arrow: "Arrow"):
        self._arrows.remove(arrow)
        # TODO: do we need a specialised arrows widget?
        self._plants_layout.removeWidget(arrow.widget)

        arrow.remove()
        self.update_render()

    def remove(self):
        self._garden = None
        self.widget.deleteLater()

    @cached_property
    def widget(self) -> QWidget:
        content = QWidget()

        layout = QVBoxLayout()

        content.setLayout(layout)

        def add_new_plant():
            self.add_plant(Plant())

        add_plant = QPushButton("Add Plant")
        add_plant.clicked.connect(add_new_plant)

        def add_new_label():
            self.add_label(Label())

        add_label = QPushButton("Add Label")
        add_label.clicked.connect(add_new_label)

        def add_new_arrow():
            self.add_arrow(Arrow())

        add_arrow = QPushButton("Add Arrow")
        add_arrow.clicked.connect(add_new_arrow)

        remove = QPushButton("Remove Bed")
        remove.clicked.connect(lambda: self._garden.remove_bed(self))

        layout.addLayout(self._form)
        layout.addWidget(add_plant)
        layout.addWidget(add_label)
        layout.addWidget(add_arrow)
        layout.addLayout(self._plants_layout)
        layout.addWidget(remove)

        self._collapsible.body = content
        self._collapsible.title = self.name
        return self._collapsible

    @cached_property
    def _collapsible(self) -> Collapsible:
        return Collapsible()

    @cached_property
    def _form(self) -> QFormLayout:
        form = QFormLayout()

        # Name
        name_label = QLabel("Name:")
        name_edit = QLineEdit(self.name)

        def set_name():
            self.name = name_edit.text()

        name_edit.textEdited.connect(set_name)
        form.addRow(name_label, name_edit)

        # Position
        position_label = QLabel("Position:")
        position_layout = QHBoxLayout()

        x_label = QLabel("x =")
        x_edit = QLineEdit(str(self.position[0]))
        y_label = QLabel("y =")
        y_edit = QLineEdit(str(self.position[1]))

        position_layout.addWidget(x_label)
        position_layout.addWidget(x_edit)
        position_layout.addWidget(y_label)
        position_layout.addWidget(y_edit)

        def update_position():
            try:
                x, y = float(x_edit.text()), float(y_edit.text())
                self.position = (x, y)
            except ValueError:
                pass

        x_edit.textEdited.connect(update_position)
        y_edit.textEdited.connect(update_position)

        form.addRow(position_label, position_layout)

        return form

    @cached_property
    def _plants_layout(self) -> QVBoxLayout:
        return QVBoxLayout()

    @cached_property
    def renderable(self) -> Renderable:
        self._rendered = True
        return Bed.Renderable(self)

    def serialise(self) -> dict:
        return {
            "name": self.name,
            "position": list(self.position),
            "plants": [plant.serialise() for plant in self.plants],
            "labels": [label.serialise() for label in self.labels],
            "arrows": [arrow.serialise() for arrow in self.arrows],
        }

    @staticmethod
    def deserialise(json: dict) -> "Bed":
        bed = Bed()

        bed.name = json["name"]
        bed.position = tuple(json["position"])

        for plant in json["plants"]:
            bed.add_plant(Plant.deserialise(plant))

        for label in json["labels"]:
            bed.add_label(Label.deserialise(label))

        for arrow in json["arrows"]:
            bed.add_arrow(Arrow.deserialise(arrow))

        return bed


class Plant:
    class Renderable(Renderable):
        BORDER_THICKNESS = 0.015

        def __init__(self, plant: "Plant"):
            super().__init__()

            self.plant = plant

        def render(self, camera: Camera):
            radius = self.plant.size
            # TODO: use an unfilled circle to make the border align better with the rest
            #       of the plant
            camera.circle(
                self.plant.position, radius + self.BORDER_THICKNESS, (0, 0, 0)
            )
            camera.circle(
                self.plant.position, radius - self.BORDER_THICKNESS, self.plant.colour
            )

    def __init__(self):
        self._bed: Optional[Bed] = None

        self._name = ""
        self._size = 0.1
        self._position = (0.0, 0.0)
        self._colour = (0, 64, 128)

        self._rendered = False

    def update_render(self):
        if self._rendered:
            self.bed.update_render()

    @property
    def bed(self) -> Bed:
        assert self._bed is not None
        return self._bed

    @bed.setter
    def bed(self, bed: Bed):
        assert isinstance(bed, Bed)
        assert self._bed is None

        self._bed = bed

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self.update_render()

    @property
    def size(self) -> float:
        return self._size

    @size.setter
    def size(self, size: float):
        self._size = size
        self.update_render()

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, position: Tuple[float, float]):
        self._position = position
        self.update_render()

    @property
    def colour(self) -> Tuple[int, int, int]:
        return self._colour

    @colour.setter
    def colour(self, colour: Tuple[int, int, int]):
        self._colour = colour
        self.update_render()

    def remove(self):
        self._garden = None
        self.widget.deleteLater()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addLayout(self._form)

        remove = QPushButton("Remove Plant")
        remove.clicked.connect(lambda: self._bed.remove_plant(self))

        layout.addWidget(remove)

        return widget

    @cached_property
    def _form(self) -> QFormLayout:
        form = QFormLayout()

        # Name
        name_label = QLabel("Name:")
        name_edit = QLineEdit(self.name)

        def set_name():
            self.name = name_edit.text()

        name_edit.textEdited.connect(set_name)
        form.addRow(name_label, name_edit)

        # Size
        size_label = QLabel("Size:")
        size_edit = QLineEdit(str(self.size))

        def update_size():
            try:
                size = float(size_edit.text())
                self.size = size
            except ValueError:
                pass

        size_edit.textEdited.connect(update_size)
        form.addRow(size_label, size_edit)

        # Position
        position_label = QLabel("Position:")
        position_layout = QHBoxLayout()

        x_label = QLabel("x =")
        x_edit = QLineEdit(str(self.position[0]))
        y_label = QLabel("y =")
        y_edit = QLineEdit(str(self.position[1]))

        position_layout.addWidget(x_label)
        position_layout.addWidget(x_edit)
        position_layout.addWidget(y_label)
        position_layout.addWidget(y_edit)

        def update_position():
            try:
                x, y = float(x_edit.text()), float(y_edit.text())
                self.position = (x, y)
            except ValueError:
                pass

        x_edit.textEdited.connect(update_position)
        y_edit.textEdited.connect(update_position)

        form.addRow(position_label, position_layout)

        # Colour
        colour_label = QLabel("Colour:")
        colour_layout = QHBoxLayout()

        red = build_colour_slider("red", colour_layout, self._colour[0])
        green = build_colour_slider("green", colour_layout, self._colour[1])
        blue = build_colour_slider("blue", colour_layout, self._colour[2])

        def update_colour():
            self.colour = (red.value(), green.value(), blue.value())

        red.valueChanged.connect(update_colour)
        green.valueChanged.connect(update_colour)
        blue.valueChanged.connect(update_colour)

        form.addRow(colour_label, colour_layout)

        return form

    @cached_property
    def renderable(self) -> Renderable:
        self._rendered = True
        return Plant.Renderable(self)

    def serialise(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "position": list(self.position),
            "colour": list(self.colour),
        }

    @staticmethod
    def deserialise(json: dict) -> "Plant":
        plant = Plant()

        plant.name = json["name"]
        plant.size = json["size"]
        plant.position = tuple(json["position"])
        plant.colour = tuple(json["colour"])

        return plant


class Label:
    class Renderable(Renderable):
        def __init__(self, label: "Label"):
            super().__init__()

            self.label = label

        def render(self, camera: Camera):
            camera.text(
                self.label.position, self.label.label, self.label.size, (0, 0, 0)
            )

    def __init__(self):
        self._bed: Optional[Bed] = None

        self._label = ""
        self._size = 0.1
        self._position = (0.0, 0.0)

        self._rendered = False

    def update_render(self):
        if self._rendered:
            self.bed.update_render()

    @property
    def bed(self) -> Bed:
        assert self._bed is not None
        return self._bed

    @bed.setter
    def bed(self, bed: Bed):
        assert isinstance(bed, Bed)
        assert self._bed is None

        self._bed = bed

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label
        self.update_render()

    @property
    def size(self) -> float:
        return self._size

    @size.setter
    def size(self, size: float):
        self._size = size
        self.update_render()

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, position: Tuple[float, float]):
        self._position = position
        self.update_render()

    def remove(self):
        self._garden = None
        self.widget.deleteLater()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addLayout(self._form)

        remove = QPushButton("Remove Label")
        remove.clicked.connect(lambda: self._bed.remove_label(self))

        layout.addWidget(remove)

        return widget

    @cached_property
    def _form(self) -> QFormLayout:
        form = QFormLayout()

        # Label
        label_label = QLabel("Label:")
        label_edit = QLineEdit(self.label)

        def set_label():
            self.label = label_edit.text()

        label_edit.textEdited.connect(set_label)
        form.addRow(label_label, label_edit)

        # Size
        size_label = QLabel("Size:")
        size_edit = QLineEdit(str(self.size))

        def update_size():
            try:
                size = float(size_edit.text())
                self.size = size
            except ValueError:
                pass

        size_edit.textEdited.connect(update_size)
        form.addRow(size_label, size_edit)

        # Position
        position_label = QLabel("Position:")
        position_layout = QHBoxLayout()

        x_label = QLabel("x =")
        x_edit = QLineEdit(str(self.position[0]))
        y_label = QLabel("y =")
        y_edit = QLineEdit(str(self.position[1]))

        position_layout.addWidget(x_label)
        position_layout.addWidget(x_edit)
        position_layout.addWidget(y_label)
        position_layout.addWidget(y_edit)

        def update_position():
            try:
                x, y = float(x_edit.text()), float(y_edit.text())
                self.position = (x, y)
            except ValueError:
                pass

        x_edit.textEdited.connect(update_position)
        y_edit.textEdited.connect(update_position)

        form.addRow(position_label, position_layout)

        return form

    @cached_property
    def renderable(self) -> Renderable:
        self._rendered = True
        return Label.Renderable(self)

    def serialise(self) -> dict:
        return {"label": self.label, "size": self.size, "position": list(self.position)}

    @staticmethod
    def deserialise(json: dict) -> "Label":
        label = Label()

        label.label = json["label"]
        label.size = json["size"]
        label.position = tuple(json["position"])

        return label


class Arrow:
    class Renderable(Renderable):
        def __init__(self, arrow: "Arrow"):
            super().__init__()

            self.arrow = arrow

        def render(self, camera: Camera):
            camera.line(self.arrow.start, self.arrow.end, 2, (0, 0, 0))

    def __init__(self):
        self._bed: Optional[Bed] = None

        self._start = (0.0, 0.0)
        self._end = (0.0, 0.0)

        # TODO: add width

        self._rendered = False

    def update_render(self):
        if self._rendered:
            self.bed.update_render()

    @property
    def bed(self) -> Bed:
        assert self._bed is not None
        return self._bed

    @bed.setter
    def bed(self, bed: Bed):
        assert isinstance(bed, Bed)
        assert self._bed is None

        self._bed = bed

    @property
    def start(self) -> Tuple[float, float]:
        return self._start

    @start.setter
    def start(self, start: Tuple[float, float]):
        self._start = start
        self.update_render()

    @property
    def end(self) -> Tuple[float, float]:
        return self._end

    @end.setter
    def end(self, end: Tuple[float, float]):
        self._end = end
        self.update_render()

    def remove(self):
        self._garden = None
        self.widget.deleteLater()

    @cached_property
    def widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addLayout(self._form)

        remove = QPushButton("Remove Arrow")
        remove.clicked.connect(lambda: self._bed.remove_arrow(self))

        layout.addWidget(remove)

        return widget

    @cached_property
    def _form(self) -> QFormLayout:
        form = QFormLayout()

        # Start
        start_label = QLabel("Start:")
        start_layout = QHBoxLayout()

        start_x_label = QLabel("x =")
        start_x_edit = QLineEdit(str(self.start[0]))
        start_y_label = QLabel("y =")
        start_y_edit = QLineEdit(str(self.start[1]))

        start_layout.addWidget(start_x_label)
        start_layout.addWidget(start_x_edit)
        start_layout.addWidget(start_y_label)
        start_layout.addWidget(start_y_edit)

        def update_start():
            try:
                x, y = float(start_x_edit.text()), float(start_y_edit.text())
                self.start = (x, y)
            except ValueError:
                pass

        start_x_edit.textEdited.connect(update_start)
        start_y_edit.textEdited.connect(update_start)

        form.addRow(start_label, start_layout)

        # End
        end_label = QLabel("End:")
        end_layout = QHBoxLayout()

        end_x_label = QLabel("x =")
        end_x_edit = QLineEdit(str(self.end[0]))
        end_y_label = QLabel("y =")
        end_y_edit = QLineEdit(str(self.end[1]))

        end_layout.addWidget(end_x_label)
        end_layout.addWidget(end_x_edit)
        end_layout.addWidget(end_y_label)
        end_layout.addWidget(end_y_edit)

        def update_end():
            try:
                x, y = float(end_x_edit.text()), float(end_y_edit.text())
                self.end = (x, y)
            except ValueError:
                pass

        end_x_edit.textEdited.connect(update_end)
        end_y_edit.textEdited.connect(update_end)

        form.addRow(end_label, end_layout)

        return form

    @cached_property
    def renderable(self) -> Renderable:
        self._rendered = True
        return Arrow.Renderable(self)

    def serialise(self) -> dict:
        return {"start": list(self.start), "end": list(self.end)}

    @staticmethod
    def deserialise(json: dict) -> "Arrow":
        arrow = Arrow()

        arrow.start = tuple(json["start"])
        arrow.end = tuple(json["end"])

        return arrow
