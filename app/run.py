from typing import Optional

from qt import QApplication, QMainWindow

from app.splash import Splash


class RuntimeEnvironment:
    # For a window to stay open, we need to keep a reference to it.  Therefore, when a
    # window is opened from within a callback, its reference should be stored here
    window: Optional[QMainWindow] = None


def run():
    app = QApplication([])

    RuntimeEnvironment.window = Splash()

    app.exec()
