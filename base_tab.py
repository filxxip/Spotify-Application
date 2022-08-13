from PyQt5.QtWidgets import (
    QDialog,
    QTabWidget,
)
from base_component import BaseForAll
from PyQt5.QtCore import Qt


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
