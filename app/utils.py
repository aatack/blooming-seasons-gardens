from os.path import isfile
from typing import Tuple

from qt import QColor, QFileDialog, QLayout, QMessageBox, QSlider, Qt, QWidget


def set_widget_background(widget: QWidget, colour: Tuple[int, int, int]):
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    palette.setColor(widget.backgroundRole(), QColor(*colour))
    widget.setPalette(palette)


def build_colour_slider(colour: str, parent: QLayout, initial_value: int) -> QSlider:
    slider = QSlider(Qt.Horizontal)
    parent.addWidget(slider)

    slider.setStyleSheet(
        "QSlider::handle:horizontal {background-color: " + colour + "}"
    )

    slider.setMinimum(0)
    slider.setMaximum(255)
    slider.setSingleStep(1)
    slider.setValue(initial_value)

    return slider


def create_new_garden():
    raise NotImplementedError()


def open_existing_garden():
    path = QFileDialog.getExistingDirectory()

    assert not path.endswith("/")
    path += "/"

    if not isfile(path + "garden.bsg"):
        error = QMessageBox()
        error.setIcon(QMessageBox.Critical)
        error.setText("Could not load garden")
        error.setInformativeText(
            f"Tried to load a folder that is not a garden: '{path}'.  A folder that "
            "contains a garden will have a file called 'garden.bsg' inside it."
        )
        error.setWindowTitle("Error")
        error.exec()

    else:
        from app.run import RuntimeEnvironment
        from app.window import Window

        if RuntimeEnvironment.window is not None:
            RuntimeEnvironment.window.close()

        RuntimeEnvironment.window = Window(path)
