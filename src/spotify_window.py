import enum
from PyQt5.QtWidgets import (
    QDialog,
    QTabWidget,
    QLabel,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QFormLayout,
    QScrollArea,
    QGroupBox,
    QWidget,
    QLineEdit,
)
from pathlib import Path
import urllib3.request
import urllib.request

# from urllib3.exceptions import DependencyWarning
# from urllib3 import disable_warnings
# disable_warnings(DependencyWarning)
import json

# import requests
from PIL import Image, ImageQt
from io import BytesIO
from .base_component import BaseForAll
from .components import MyButtonwithImage, MyLabelwithText
from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal, QObject, QUrl
import os
from .videowidget import CustomVideoPlayer
from PyQt5.QtGui import QPixmap, QIcon, QImage
from .firstwindow import FirstTab
from .downloadwindow import SecondTab


class SpotifyWindow:
    dimensions = (800, 800)

    def __init__(self, master):
        self.master = master
        self.window = QTabWidget()
        self.window.tabBar().setCursor(Qt.OpenHandCursor)
        self.master.set_dimentions(*self.dim)
        self.window.dimensions = self.dim
        self.tab1 = FirstTab(self.master, self.window, "Player")
        self.tab2 = SecondTab(self.master, self.window, "Downloader", 5)
        # self.window.setCurrentWidget(self.tab2.tab)
        self.tab2.signal.signal.connect(
            lambda a1, a2, a3, a4: self.tab1.songs_panel.update_list(a1, a2, a3, a4)
        )
        # self.tab2.worker.signal.signal.connect(self.tab1.songs_panel.update_list)
        # self.tab3 = MyTab(self.master, self.window, "tab3")
        # self.tab4 = MyTab(self.master, self.window, "tab4")

    def post_init(self, *args):
        self.tab1.songs_panel.post_init(*args)

    @property
    def dim(self):
        return SpotifyWindow.dimensions
