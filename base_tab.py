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
import urllib3.request
import urllib.request

# from urllib3.exceptions import DependencyWarning
# from urllib3 import disable_warnings
# disable_warnings(DependencyWarning)
import json

# import requests
from PIL import Image, ImageQt
from io import BytesIO
from youtubesearchpython import VideosSearch
from base_component import BaseForAll
from components import MyButtonwithImage, MyLabelwithText
from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal, QObject, QUrl
import os
from videowidget import CustomVideoPlayer
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MyTab:
    def __init__(self, master, window, title):
        self.master: BaseForAll = master
        self.window: QTabWidget = window
        self.tab = QDialog()
        self.tab.setObjectName("tabwidget")
        self.window.addTab(self.tab, title)
        self.master.widget.setWindowState(Qt.WindowActive)

    @property
    def tabbar(self):
        return self.window.tabBar()
