from typing import Optional

from qt import QApplication, QMainWindow

from app.splash import Splash
from app.window import Window


class RuntimeEnvironment:
    # For a window to stay open, we need to keep a reference to it.  Therefore, when a
    # window is opened from within a callback, its reference should be stored here
    window: Optional[QMainWindow] = None


def run(path: Optional[str] = None):
    app = QApplication([])

    if path is None:
        RuntimeEnvironment.window = Splash()
    else:
        RuntimeEnvironment.window = Window(path)

    app.exec()
