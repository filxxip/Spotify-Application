import sys
from PyQt5.QtWidgets import (
    QApplication,
)
from base_component import BaseForAll
from open_window import OpenWindow

from spotify_window import SpotifyWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = BaseForAll(app, "SPOTIFY", "style.css", SpotifyWindow)
    sys.exit(app.exec())
