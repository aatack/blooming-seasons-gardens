from typing import Optional, Set

from qt import QApplication, QMainWindow

from app.splash import Splash
from app.window import Modal, Window


class RuntimeEnvironment:
    # For a window to stay open, we need to keep a reference to it.  Therefore, when a
    # window is opened from within a callback, its reference should be stored here
    windows: Set[QMainWindow] = set()


def run(path: Optional[str] = None):
    app = QApplication([])

    def manage_modals():
        for window in list(RuntimeEnvironment.windows):
            if isinstance(window, Modal) and not window.isActiveWindow():
                window.close_modal()

    app.focusChanged.connect(manage_modals)

    if path is None:
        RuntimeEnvironment.windows.clear()
        RuntimeEnvironment.windows.add(Splash())
    else:
        RuntimeEnvironment.windows.clear()
        RuntimeEnvironment.windows.add(Window(path))

    app.exec()
