from pathlib import Path
import sys
from PyQt5.QtWidgets import (
    QApplication,
)

# from src.base_componenport OpenWindow
# from PyQt5.QtCot import BaseForAll
# from src.open_window imre import Qt
# from src.spotify_window import SpotifyWindow
# if __name__ == "__main__":
from src.base_component import BaseForAll
from src.open_window import OpenWindow
import __main__

app = QApplication(sys.argv)
w = BaseForAll(
    app,
    "SPOTIFY",
    rf"{Path(__main__.__file__).absolute().parent.__str__()}/src/style.css",
    OpenWindow,
)
sys.exit(app.exec())