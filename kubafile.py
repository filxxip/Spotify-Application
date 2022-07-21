from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle(
            "PyQt Video Player Widget Example - pythonprogramminglanguage.com"
        )
        videoWidget = QVideoWidget()
        videoWidget.setStyleSheet("background-color:blue")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
# class Window(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#         layout = QGridLayout()
#         self.setLayout(layout)
#         label1 = QLabel("Widget in Tab 1.")
#         label2 = QLabel("Widget in Tab 2.")
#         self.tabwidget = QTabWidget()
#         # self.tabwidget.addTab(View1(), "Tab 1")
#         self.tabwidget.addTab(label2, "Tab 2")
#         self.tabwidget.currentChanged.connect(self.foo)
#         layout.addWidget(self.tabwidget, 0, 0)

#     def foo(self, index):
#         self.tabwidget.getTab(index).updateTranslations()
#         print("Hello: ", index)


# app = QApplication(sys.argv)
# screen = Window()
# screen.show()
# sys.exit(app.exec_())
