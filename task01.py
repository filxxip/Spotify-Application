from dataclasses import InitVar, dataclass, field
from singleton import Singleton
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget, QLabel
import sys


class Window(QDialog):
    def __init__(self, master):
        super().__init__()
        label = QLabel()
        label.setText("dsfds")

class Singleton(type):
    instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self.instances:
            instance = type.__call__(self, *args, **kwargs)
            self.instances[self] = instance
        return self.instances[self]

@dataclass
class PhoneApp(metaclass=Singleton):
    """Singleton class which is basis for the entire app.

    Params:
        master (QApplication): main component of PyQt5 app, the __str__ method doesn't contain this variable
        title (str): title of PhoneApp application
        style_file (str): name of css file which contains all stylesheets of widgets
        first_window (object): class object which is shown when app is turned on
        height (int): height of the window, property which is initialized during the __post_init__ method
        width (int): width of the window, property which is initialized during the __post_init__ method
        widget (QStackedWidget): component which will contain every view of application, the __str__ method doesn't contain this variable and user cannot initialize it
        _windows (dict): initially empty dictionary which will contain every class as key and every instance of this class as a value, the __str__ method doesn't contain this variable and user cannot initialize it"""

    master: QApplication = field(repr=False)
    title: str
    style_file: str
    first_window: object
    height: InitVar[int]
    width: InitVar[int]
    widget: QStackedWidget = field(init=False, repr=False)
    _windows: dict = field(init=False, repr=False)

    def __post_init__(self, screen_widht: int, screen_height: int) -> None:
        """Initialize a new PhoneApp instance
        
        Params:
            screen_widht (int): width of app
            screen_height (int): height of app"""
        self.widget = QStackedWidget()
        self.master.setStyleSheet(open(self.style_file).read())
        self._windows = {}
        self.add_set_widget(self.first_window, screen_widht, screen_height)
        self.widget.show()

    @property
    def height(self) -> int:
        """Property which provides a height of app

        Returns:
            height of the app"""
        return self.widget.height()

    @property
    def width(self) -> int:
        """Property which provides a width of app

        Returns:
            width of the app"""
        return self.widget.width()

    @height.setter
    def height(self, new_height: int) -> None:
        """Setter which sets new height of app"""
        self.widget.setFixedHeight(new_height)


    @width.setter
    def width(self, new_width: int) -> None:
        """Setter which sets new width of app"""
        self.widget.setFixedWidth(new_width)

    def set_measures(self, new_width: int, new_height: int) -> None:
        """Method which sets new height and width of app
        
        Params:
            widht (int): new widht of app window
            height (int): new height of app window"""
        self.width = new_width
        self.height = new_height

    def add_widget(self, new_widget: object) -> None:
        """Method which adds new class object to the dictionary, if dictionary already contains this class, it is replaced with a new one
        
        Params:
            widget (object): class object which is setted on current widget"""
        widget = new_widget(self)
        if self._windows.get(new_widget.__name__):
            del self._windows[new_widget.__name__]
        self._windows[new_widget.__name__] = widget
        self.widget.addWidget(widget)

    def set_widget(self, widget: object, width: int = 0, height: int = 0) -> None:
        """Method which sets new class object on current widget

        Params:
            widget (object): class object which is setted on current widget
            widht (int): new widht of app window, if not passed, then it doesn't change the width
            height (int): new height of app window, if not passed, then it doesn't change the height"""
        if width:
            self.width = width
        if height:
            self.height = height
        name = widget.__name__
        self.widget.setCurrentWidget(self._windows.get(name))

    def add_set_widget(self, new_widget: object, width: int = 0, height: int = 0):
        """Method which adds new class object to the dictionary and also sets it as current widget, if dictionary already contains this class, it is replaced with a new one
        
        Params:
            widget (object): class object which added to dictionary and setted on current widget
            widht (int): new widht of app window, if not passed, then it doesn't change the width
            height (int): new height of app window, if not passed, then it doesn't change the height"""
        self.add_widget(new_widget)
        self.set_widget(new_widget, width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PhoneApp(app, "SPOTIFY", "style.css", Window, 1000, 800)
    sys.exit(app.exec())
