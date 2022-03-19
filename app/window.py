from qt import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.status = QStatusBar()
        self.widget = QWidget()

        self.setCentralWidget(self.widget)
        self.setStatusBar(self.status)

        self._populate_content()

    def _populate_content(self):
        status_button = QPushButton("Status button")
        self.status.addWidget(status_button)

        l1 = QLabel("Name")
        nm = QLineEdit()

        l2 = QLabel("Address")
        add1 = QLineEdit()
        add2 = QLineEdit()
        fbox = QFormLayout()
        fbox.addRow(l1, nm)
        vbox = QVBoxLayout()

        vbox.addWidget(add1)
        vbox.addWidget(add2)
        fbox.addRow(l2, vbox)
        hbox = QHBoxLayout()

        r1 = QRadioButton("Male")
        r2 = QRadioButton("Female")
        hbox.addWidget(r1)
        hbox.addWidget(r2)
        hbox.addStretch()
        fbox.addRow(QLabel("sex"), hbox)
        submit = QPushButton("Submit")
        fbox.addRow(submit, QPushButton("Cancel"))
        submit.clicked.connect(lambda: self.status.showMessage("Submitted", 500))

        self.widget.setLayout(fbox)
