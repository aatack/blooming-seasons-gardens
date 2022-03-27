from qt import QApplication

from app.splash import Splash
from app.window import Window


def run():
    app = QApplication([])

    # window = Window("tmp/Garden A/")
    splash = Splash()

    app.exec()
