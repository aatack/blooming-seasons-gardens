from qt import QApplication

from app.garden import Garden
from app.window import Window


def run():
    app = QApplication([])

    window = Window(Garden.read("tmp/garden.json"))
    window.resize(1000, 800)
    window.setWindowTitle("Blooming Seasons Design Studio")

    window.show()
    app.exec()
