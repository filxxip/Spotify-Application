from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QCheckBox,
)
from PyQt5.QtGui import QPixmap, QIcon, QCursor
import json
from enum import Enum


class Widget_index(Enum):
    MAIN: 0
    SECOND: 1


class MyError(Exception):
    def __init__(self, text):

        with open("json_files/data_main_window.json") as file:
            data = json.load(file)["messagebox_red"]
        MyMsgBox(
            text=f"Logged in failed, {text}",
            **data,
            OK=[QMessageBox.AcceptRole, lambda: None],
        )


class State(Enum):
    NORMAL = 1
    INNORMAL = 2


class MyCheckBox:
    def __init__(
        self,
        master,
        name,
        position_x,
        position_y,
        width,
        height,
        text,
        function=lambda: None,
    ):
        self.checkbox = QCheckBox(text, master)
        self.checkbox.setObjectName(name)
        self.checkbox.setGeometry(position_x, position_y, width, height)
        self.checkbox.stateChanged.connect(function)

    @property
    def state(self):
        return self.checkbox.isChecked()

    @state.setter
    def state(self, value):
        if value:
            self.checkbox.setCheckState(2)
        else:
            self.checkbox.setCheckState(0)


class MyLabel:
    def __init__(
        self,
        master,
        position_x,
        position_y,
        width,
        height,
        name,
        name2=None,
    ):
        self.label = QLabel(master)
        self.label.setGeometry(position_x, position_y, width, height)
        self.label.setObjectName(name)


class MyLabelwithText(MyLabel):
    def __init__(
        self,
        master,
        position_x,
        position_y,
        width,
        height,
        name,
        text=None,
        name2=None,
        text_align=Qt.AlignLeft,
    ):
        super().__init__(master, position_x, position_y, width, height, name, name2)
        if text:
            self.label.setText(text)
            self.label.setAlignment(text_align)


class MyLabelwithImage(MyLabel):
    def __init__(
        self,
        master,
        position_x,
        position_y,
        width,
        height,
        name,
        image1=None,
        image2=None,
        name2=None,
    ):
        super().__init__(master, position_x, position_y, width, height, name, name2)
        self.setting_images(master, width, image1, image2, name2)

    def setting_images(self, master, width, image, image2, name2):
        if image:
            self.pixmap1 = QPixmap(image)
            self.pixmap1 = self.pixmap1.scaledToWidth(width)
            self.label.setPixmap(self.pixmap1)
        if image2:
            self.pixmap2 = QIcon(image2)
            # self.name2 = name2
            self.hover = False
            self.label.installEventFilter(master)
            self.pixmap2 = QPixmap(image)
            self.pixmap2 = self.pixmap2.scaledToWidth(width)

    def change_style(self):
        if not self.hover:
            self.hover = True
            self.label.setPixmap(self.pixmap2)
        else:
            self.hover = False
            self.label.setPixmap(self.pixmap1)


class MyButton:
    def __init__(
        self,
        master,
        position_x,
        position_y,
        width,
        height,
        name,
        function_clicked=None,
        function_pressed=None,
        function_released=None,
        name2=None,
    ):
        self.name = name
        self.button = QPushButton(master)
        # self.button.
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setGeometry(position_x, position_y, width, height)
        self.button.setObjectName(name)
        if function_clicked:
            self.button.clicked.connect(function_clicked)
            self.function_clicked = function_clicked
        if function_pressed:
            self.button.pressed.connect(function_pressed)
            self.function_pressed = function_pressed
        if function_released:
            self.button.released.connect(function_released)
            self.function_released = function_released

    def change_function_clicked(self, new_func):
        self.button.clicked.connect(new_func)


class Mybuttonwithtext(MyButton):
    def __init__(
        self,
        master,
        position_x,
        position_y,
        width,
        height,
        name,
        function_clicked=None,
        function_pressed=None,
        function_released=None,
        text=None,
        name2=None,
    ):
        super().__init__(
            master,
            position_x,
            position_y,
            width,
            height,
            name,
            function_clicked,
            function_pressed,
            function_released,
            name2,
        )
        if text:
            self.button.setText(text)


class MyButtonwithImage(MyButton):
    def __init__(
        self,
        master,
        position_x,
        position_y,
        width,
        height,
        name,
        function_clicked=None,
        function_pressed=None,
        function_released=None,
        image=None,
        name2=None,
        image2=None,
    ):
        super().__init__(
            master,
            position_x,
            position_y,
            width,
            height,
            name,
            function_clicked,
            function_pressed,
            function_released,
            name2,
        )
        self.setting_images(master, width, height, image, image2, name2)

    def setting_images(self, master, width, height, image, image2, name2):
        if image:
            self.button.setIconSize(QSize(width, height))

            self.icon1 = QIcon(image)
            self.button.setIcon(self.icon1)
        if image2:
            self.icon2 = QIcon(image2)
            # self.name2 = name2
            self.hover = False
            self.button.installEventFilter(master)

    def change_style(self):
        if not self.hover:
            self.hover = True
            self.button.setIcon(self.icon2)
        else:
            self.hover = False
            self.button.setIcon(self.icon1)


class MyEntry:
    def __init__(
        self, master, position_x, position_y, width, height, name, placeholder=None
    ):
        self.entry = QLineEdit(master)
        self.entry.setGeometry(position_x, position_y, width, height)
        self.entry.setObjectName(name)
        if placeholder:
            self.entry.setPlaceholderText(placeholder)


class MyEntryPassword(MyEntry):
    def __init__(
        self,
        master,
        position_x,
        position_y,
        width,
        height,
        name,
        placeholder=None,
        see_button=False,
    ):
        super().__init__(
            master, position_x, position_y, width, height, name, placeholder
        )
        self.entry.setEchoMode(QLineEdit.Password)
        if see_button:
            self.create_see_button(master, width, name, position_x, position_y)

    def create_see_button(self, master, width, name, x, y):
        def press():
            self.entry.setObjectName("no_password")
            self.entry.style().polish(self.entry)
            self.entry.setEchoMode(QLineEdit.Normal)

        def release():
            self.entry.setObjectName(name)
            self.entry.style().polish(self.entry)
            self.entry.setEchoMode(QLineEdit.Password)

        self.button = Mybuttonwithtext(
            master,
            x + width + 30,
            y,
            100,
            30,
            "see_password",
            function_pressed=press,
            function_released=release,
            text="SEE",
        )


class Label_Entry_Box:
    def __init__(
        self,
        master,
        position_x,
        position_y,
        widthlabel,
        widthentry,
        height,
        namelabel,
        nameentry,
        text,
        password_style=False,
        see_button=False,
        placeholder=False,
    ):
        self.labelname = namelabel
        self.entryname = nameentry
        self._label = MyLabelwithText(
            master,
            position_x,
            position_y,
            widthlabel,
            height,
            namelabel,
            text,
            text_align=Qt.AlignCenter,
        )
        if password_style:
            self._entry = MyEntryPassword(
                master,
                position_x + widthlabel + 20,
                position_y,
                widthentry,
                height,
                nameentry,
                placeholder,
                see_button,
            )
        else:
            self._entry = MyEntry(
                master,
                position_x + widthlabel + 20,
                position_y,
                widthentry,
                height,
                nameentry,
                placeholder,
            )

    @property
    def entry(self):
        return self._entry.entry

    @entry.setter
    def entry(self, value):
        self._entry.entry.setText(value)

    @property
    def label(self):
        return self._label.label

    def __str__(self):
        return self.entry.text()

    def clear(self):
        self.entry.setText("")

    def __eq__(self, other):
        return self.entry.text() == other

    def __bool__(self):
        return bool(self.entry.text())


class Label_Entry_Box_Name(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        return (
            True
            if self.__str__() == self.__str__().capitalize() and self.__str__()
            else False
        )


class Label_Entry_Box_Age(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        return True if self.__str__().isdigit() and self.__str__() else False


class Label_Entry_Box_Surname(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        return (
            True
            if self.__str__() == self.__str__().capitalize() and self.__str__()
            else False
        )


class Label_Entry_Box_Nationality(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        return (
            True
            if self.__str__() == self.__str__().capitalize() and self.__str__()
            else False
        )


class Label_Entry_Box_Country(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        return (
            True
            if self.__str__() == self.__str__().capitalize() and self.__str__()
            else False
        )


class Label_Entry_Box_Login(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        with open("json_files/file.json") as file:
            file = json.load(file)
            data = [log["login"] for log in file]
        return False if self.__str__() in data or not self.__str__() else True


class Label_Entry_Box_Password(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        return any(ele.isupper() for ele in self.__str__())  # checking data


class Label_Entry_Box_Gender(Label_Entry_Box):
    def check(
        self,
    ) -> bool:
        return (
            True if self.__str__() in ("male", "female") and self.__str__() else False
        )


class LoginBox:
    def __init__(self, master, x, y, text, password_style=False):
        self.create_label(master, x, y, text, password_style)
        self.create_entry(master, x, y, password_style)

    def create_label(self, master, x, y, text, password_style):
        self.label = QLabel(master)
        if not password_style:
            self.label.setObjectName("login_label")
        else:
            self.label.setObjectName("password_label")
        self.label.setText(text.upper())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(x, y, 100, 30)

    def create_entry(self, master, x, y, password_style):
        self.entry = QLineEdit(master)
        self.entry.setGeometry(x + 120, y, 100, 30)
        if password_style:
            self.entry.setPlaceholderText("your pass")
            self.entry.setObjectName("password_entry")
            self.entry.setEchoMode(QLineEdit.Password)
            self.create_see_button(master, x, y)
        else:
            self.entry.setObjectName("login_entry")
            self.entry.setPlaceholderText("your login")

    def create_see_button(self, master, x, y):
        def press():
            self.entry.setObjectName("no_password")
            self.entry.style().polish(self.entry)
            self.entry.setEchoMode(QLineEdit.Normal)

        def release():
            self.entry.setObjectName("password_entry")
            self.entry.style().polish(self.entry)
            self.entry.setEchoMode(QLineEdit.Password)

        self.button = QPushButton(master)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setText("SEE")
        self.button.setObjectName("see_password")
        self.button.pressed.connect(press)
        self.button.released.connect(release)
        self.button.setGeometry(x + 250, y, 100, 30)

    def __str__(self):
        return self.entry.text()


class MyMsgBox:
    def __init__(self, title, text, name, icon, **options):
        self.creating_elements(title, name, text, icon)
        self.items = []
        self.adding_buttons(options)
        self.message.exec()
        functions = (i[1] for i in options.values())
        for item, func in zip(self.items, functions):
            if self.message.clickedButton() == item:
                func()
                break

    def creating_elements(self, title, name, text, icon):
        self.message = QMessageBox()
        self.message.setWindowTitle(title)
        self.message.setText(text)
        self.message.setObjectName(name)
        self.message.setIconPixmap(QPixmap(icon).scaledToWidth(40))

    def adding_buttons(self, options):
        for item in options.keys():
            opt = self.message.addButton(item, options[item][0])
            self.items.append(opt)
