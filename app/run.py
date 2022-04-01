from typing import Optional, Set

from qt import QApplication, QMainWindow

from app.splash import Splash
from app.window import Window


class RuntimeEnvironment:
    # For a window to stay open, we need to keep a reference to it.  Therefore, when a
    # window is opened from within a callback, its reference should be stored here
    windows: Set[QMainWindow] = set()


def run(path: Optional[str] = None):
    app = QApplication([])

    if path is None:
        RuntimeEnvironment.windows.clear()
        RuntimeEnvironment.windows.add(Splash())
    else:
        RuntimeEnvironment.windows.clear()
        RuntimeEnvironment.windows.add(Window(path))

    app.exec()
