from qt import QApplication

from app.window import Window


def run():
    app = QApplication([])

    window = Window("tmp/Garden A/")
    window.resize(1000, 800)
    window.setWindowTitle("Blooming Seasons Design Studio")

    window.show()
    app.exec()
