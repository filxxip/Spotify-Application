from singleton import Singleton
from PyQt5.QtWidgets import QStackedWidget


class BaseForAll(metaclass=Singleton):
    def __init__(self, master, title, styling, starting_window):
        self.master = master
        master.setStyleSheet(open(styling).read())
        self.windows = {}
        self.widget = QStackedWidget()
        self.widget.setWindowTitle(title)
        self._height = 0
        self._width = 0
        self.add_and_set(starting_window)
        self.show()

    def set_dimentions(self, width, height, minimum_width = False, maximum_width = False, minimum_height = False, maximum_height = False):
        self.height = height
        self.width = width
        if minimum_height:
            self.widget.setMinimumHeight(minimum_height)
        if maximum_height:
            self.widget.setMaximumHeight(maximum_height)
        if minimum_width:
            self.widget.setMinimumWidth(minimum_width)
        if maximum_width:
            self.widget.setMaximumWidth(maximum_width)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, new_value):
        self._width = new_value
        self.widget.setFixedWidth(new_value)

    @height.setter
    def height(self, new_value):
        self._height = new_value
        self.widget.setFixedHeight(new_value)

    def add_widget(self, new_widget):
        if self.windows.get(new_widget.__name__):
            self.widget.removeWidget(self.windows[new_widget.__name__])
            del self.windows[new_widget.__name__]
        w = new_widget(self)
        self.windows[new_widget.__name__] = w.window
        self.widget.addWidget(w.window)

    def set_widget(self, widget):
        name = widget.__name__
        self.set_dimentions(*widget.dimensions)
        self.widget.setCurrentWidget(self.windows.get(name))

    def add_and_set(self, new_widget):
        self.add_widget(new_widget)
        self.set_widget(new_widget)

    def show(self):
        self.widget.show()
