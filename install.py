from pathlib import Path
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QLabel,
    QWidget,
    QComboBox,
    QPushButton,
    QFileDialog,
)
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QIcon, QPixmap
import __main__


class Window:
    def __init__(self):
        self.master = QWidget()
        self.master.setGeometry(200, 200, 400, 400)
        self.mainlayout = QVBoxLayout(self.master)
        # self.mainlayout.setAlignment(Qt.AlignCenter)
        self.mainlayout.setContentsMargins(40, 40, 40, 40)
        self.creation_label()
        self.creation_combobox()
        self.create_install_button()
        self.master.setLayout(self.mainlayout)
        self.master.show()

    def creation_label(self):
        image = "images/spot.jpg"
        image = QPixmap(f"{Path(__main__.__file__).parent.__str__()}/{image}")
        image = image.scaledToWidth(400)
        label = QLabel()
        label.setMaximumHeight(120)
        label.setObjectName("image_with_background")
        label.setPixmap(image)
        self.mainlayout.addWidget(label, 1)

    def creation_combobox(self):
        self.combobox = QComboBox()
        self.combobox.addItem("Linux Ubuntu")
        self.combobox.addItem("Linux")
        self.combobox.addItem("Windows 10")
        self.combobox.addItem("Windows 7")
        self.mainlayout.addWidget(self.combobox, 19)

    def create_install_button(self):
        self.button = QPushButton()
        self.button.setObjectName("songs")
        self.button.setFixedWidth(100)
        self.button.setContentsMargins(100, 0, 100, 0)
        self.button.setText("INSTALL")
        self.mainlayout.addWidget(self.button, alignment=Qt.AlignHCenter)
        self.button.clicked.connect(self.function)

    def function(self):
        directory = QFileDialog.getExistingDirectory(
            self.master, "Set shortcut place", QDir.homePath()
        )
        if directory:
            import os

            # print(fr'{Path(__main__.__file__).absolute().parent.__str__()}/.install_linux_ubuntu.sh')
            org = rf"{Path(__main__.__file__).absolute().parent.__str__()}/main.sh"
            new = rf"{directory}/spotify.sh"
            # print(org, new, sep = "\n")
            import shutil

            shutil.copyfile(org, new)
            os.system(f"chmod +x {new}")
            if self.combobox.currentText() == "Linux Ubuntu":
                ...
            # os.system(fr'./{Path(__main__.__file__).absolute().parent.__str__()}/.install_linux_ubuntu.sh')
            else:
                print("wait")


app = QApplication(sys.argv)
styling = rf"{Path(__main__.__file__).absolute().parent.__str__()}/src/style.css"
app.setStyleSheet(open(styling).read())
window = Window()
sys.exit(app.exec())
