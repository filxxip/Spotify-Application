import sys
from PyQt5.QtWidgets import (
    QApplication,
)
from base_component import BaseForAll
from open_window import OpenWindow
from PyQt5.QtCore import Qt
from spotify_window import SpotifyWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("cos")
    w = BaseForAll(app, "SPOTIFY", "style.css", OpenWindow)
    print("cos2")
    sys.exit(app.exec())
