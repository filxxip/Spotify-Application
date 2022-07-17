import sys
from PyQt5.QtCore import Qt, QSize, QEvent, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QDialog,
    QStackedWidget,
)
from PyQt5.QtGui import QPixmap, QIcon, QCursor
import json
from enum import Enum

from components import (
    Label_Entry_Box,
    Label_Entry_Box_Age,
    Label_Entry_Box_Country,
    Label_Entry_Box_Gender,
    Label_Entry_Box_Login,
    Label_Entry_Box_Name,
    Label_Entry_Box_Nationality,
    Label_Entry_Box_Password,
    Label_Entry_Box_Surname,
    MyButtonwithImage,
    MyCheckBox,
    MyError,
    MyLabelwithImage,
    MyLabelwithText,
    MyMsgBox,
    Mybuttonwithtext,
    State,
)
from blocking_decorator import blocked_button


class Widget_index(Enum):
    MAIN: 0
    SECOND: 1


class MainWindow:
    def __init__(self):
        self.window = QDialog()
        self.window.eventFilter = self.eventFilter
        self.window.setGeometry(100, 100, 500, 500)
        with open("json_files/data_main_window.json") as data:
            data = json.load(data)
        self.window.setWindowTitle(data["title_window"])
        self.cancel_button = MyButtonwithImage(
            self.window,
            function_clicked=lambda: self.func_for_exit(
                data["message_box_cancel_window"]
            ),
            **data["cancel_button"],
        )
        self.title_label = MyLabelwithImage(self.window, **data["title_label"])
        self.login = Label_Entry_Box(self.window, **data["login_entry_box"])
        self.password = Label_Entry_Box(self.window, **data["password_entry_box"])
        self.password.entry.returnPressed.connect(
            lambda: self.submit_command(data["messagebox_green"])
        )
        self.submit_button = Mybuttonwithtext(
            self.window,
            function_clicked=lambda: self.submit_command(data["messagebox_green"]),
            **data["submit_button"],
        )
        self.checkbox = MyCheckBox(self.window, **data["remember_check_box"])
        self.entry_setter()
        self.window.show()

    def entry_setter(self):
        with open("json_files/data.json") as file:
            data = json.load(file)

        self.login.entry = data["remembered_data"]["login"]
        self.password.entry = data["remembered_data"]["password"]
        if self.login and self.password:
            self.checkbox.state = True

    def func_for_exit(self, data):
        MyMsgBox(
            **data,
            Yeah=[QMessageBox.YesRole, lambda: widget.setCurrentIndex(0)],
            Nope=[QMessageBox.NoRole, lambda: None],
        )

    def change_state(self, state=State.INNORMAL):
        def change_state_to_normal():
            self.login.entry.setObjectName("login_entry")
            self.login.entry.style().polish(self.login.entry)
            self.password.entry.setObjectName("password_entry")
            self.password.entry.style().polish(self.password.entry)

        def change_state_to_innormal():
            self.login.entry.setObjectName("incorrect_login_entry")
            self.login.entry.style().polish(self.login.entry)
            self.password.entry.setObjectName("incorrect_password_entry")
            self.password.entry.style().polish(self.password.entry)

        def change_state_to_upnormal():
            self.login.entry.setObjectName("correct_login_entry")
            self.login.entry.style().polish(self.login.entry)
            self.password.entry.setObjectName("correct_password_entry")
            self.password.entry.style().polish(self.password.entry)

        if state == State.INNORMAL:
            change_state_to_innormal()
        else:
            change_state_to_upnormal()
        QTimer.singleShot(1000, change_state_to_normal)

    def check_json(self):
        with open("json_files/data.json") as file:
            data = json.load(file)
            data2 = data["remembered_data"]
        if self.login == data2["login"] and self.password == data2["password"]:
            if not self.checkbox.state:
                with open("json_files/data.json", "w") as file:
                    data["remembered_data"] = {"login": "", "password": ""}
                    json.dump(data, file)
            return True
        if self.checkbox.state:
            data["remembered_data"] = {
                "login": str(self.login),
                "password": str(self.password),
            }
            with open("json_files/data.json", "w") as file:
                json.dump(data, file)
            return True
        return False

    @blocked_button(
        "submit_button.button",
        3,
    )
    def submit_command(self, data_message_green):
        try:
            if str(self.login) and str(self.password):
                with open("json_files/file.json") as file:
                    data = json.load(file)
                logins = [person["login"] for person in data]
                passwords = (person["password"] for person in data)
                if str(self.login) in logins:
                    login_index = logins.index(str(self.login))
                    for _ in range(login_index + 1):
                        password = next(passwords)
                    if self.password == password:
                        self.change_state(state=State.NORMAL)
                        self.check_json()
                        MyMsgBox(
                            **data_message_green,
                            OK=[QMessageBox.AcceptRole, lambda: None],
                        )

                    else:
                        self.change_state()
                        raise MyError("wrong password")
                else:
                    self.change_state()
                    raise MyError("login undefined")
                # self.password.clear()
                # self.login.clear()
            else:
                self.change_state()
                raise MyError("empty login or password")
        except MyError:
            pass

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.cancel_button.change_style()
        elif event.type() == QEvent.Leave:
            self.cancel_button.change_style()
        return False


def button_unchecked(func):
    def decor(*args, **kwargs):
        func(*args, **kwargs)


class SecondWindow:
    def __init__(self):
        self.window = QDialog()
        self.window.eventFilter = self.eventFilter
        with open("json_files/data_second_window.json") as data:
            data = json.load(data)
        self.title_label = MyLabelwithImage(self.window, **data["title_label"])
        self.exit_button = MyButtonwithImage(
            self.window,
            **data["cancel_button"],
            function_clicked=lambda: self.func_for_exit(data["exit_button"]),
        )
        self.login_label = MyLabelwithText(
            self.window,
            **data["login_label"],
            text_align=Qt.AlignCenter,
        )
        self.password_label = MyLabelwithText(
            self.window,
            **data["password_label"],
            text_align=Qt.AlignCenter,
        )
        self.login_window = MyButtonwithImage(
            self.window,
            **data["login_button"],
            function_clicked=lambda: [
                widget.setCurrentIndex(1),
                self.new_account.button.setCheckable(False),
            ],
        )
        self.new_account = MyButtonwithImage(
            self.window,
            **data["password_button"],
            function_clicked=lambda: [
                widget.setCurrentIndex(2),
                self.new_account.button.setCheckable(False),
            ],
        )

    def func_for_exit(self, data):
        MyMsgBox(
            **data,
            Yeah=[QMessageBox.YesRole, lambda: exit()],
            Nope=[QMessageBox.NoRole, lambda: None],
        )

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.exit_button.change_style()
        elif event.type() == QEvent.Leave:
            self.exit_button.change_style()
        return False


class New_Account_Window:
    def __init__(self):
        self.window = QDialog()
        self.window.eventFilter = self.eventFilter
        with open("json_files/new_account_window.json") as file:
            data = json.load(file)
        self.exit_button = MyButtonwithImage(
            self.window,
            **data["cancel_button"],
            function_clicked=lambda: self.func_for_exit(
                data["message_box_cancel_window"]
            ),
        )
        entries_data = data["entries_label_basic"]
        self.postioning_entry_login = Label_Entry_Box_Login(
            self.window, **entries_data, **data["login"]
        )
        self.postioning_entry_name = Label_Entry_Box_Name(
            self.window, **entries_data, **data["name"]
        )
        self.postioning_entry_surname = Label_Entry_Box_Surname(
            self.window, **entries_data, **data["surname"]
        )
        self.postioning_entry_age = Label_Entry_Box_Age(
            self.window, **entries_data, **data["age"]
        )
        self.postioning_entry_coutry = Label_Entry_Box_Country(
            self.window, **entries_data, **data["country"]
        )
        self.postioning_entry_nationality = Label_Entry_Box_Nationality(
            self.window, **entries_data, **data["nationality"]
        )
        self.postioning_entry_gender = Label_Entry_Box_Gender(
            self.window, **entries_data, **data["gender"]
        )
        self.postioning_entry_password = Label_Entry_Box_Password(
            self.window, **entries_data, **data["password"]
        )
        self.postioning_entry_repeat = Label_Entry_Box_Password(
            self.window, **entries_data, **data["repeat"]
        )
        for item_widget in self.__dict__:
            if item_widget.startswith("postioning_entry_"):
                getattr(self, item_widget).entry.returnPressed.connect(
                    lambda: self.submiter.button.click()
                )
        self.title_label = MyLabelwithImage(self.window, **data["title_label"])
        self.submiter = Mybuttonwithtext(
            self.window,
            **data["submit_button"],
            function_clicked=lambda: self.command_for_submit(),
        )

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.exit_button.change_style()
        elif event.type() == QEvent.Leave:
            self.exit_button.change_style()
        return False

    def func_for_exit(self, data):
        MyMsgBox(
            **data,
            Yeah=[QMessageBox.YesRole, lambda: widget.setCurrentIndex(0)],
            Nope=[QMessageBox.NoRole, lambda: None],
        )

    @blocked_button("submiter.button", 1)
    def command_for_submit(self):
        args = [
            [
                getattr(self, item_widget),
                getattr(self, item_widget).entryname,
                "new_account_login_entry_incorrect",
                "new_account_login_entry_correct",
            ]
            for item_widget in self.__dict__
            if item_widget.startswith("postioning_entry_")
        ]

        self.change_state(*args)

    def create_new_user(self):
        with open("json_files/new_account_window.json") as file:
            data = json.load(file)["messagebox_new_account"]

        MyMsgBox(**data, Great=[QMessageBox.YesRole, lambda: widget.setCurrentIndex(0)])
        with open("json_files/file.json") as file:
            data = json.load(file)
        data.append(
            {
                "name": self.postioning_entry_name.__str__(),
                "surname": self.postioning_entry_surname.__str__(),
                "login": self.postioning_entry_login.__str__(),
                "password": self.postioning_entry_password.__str__(),
                "age": self.postioning_entry_age.__str__(),
                "country": self.postioning_entry_coutry.__str__(),
                "nationality": self.postioning_entry_nationality.__str__(),
                "gender": self.postioning_entry_gender.__str__(),
            }
        )
        with open("json_files/file.json", "w") as file:
            json.dump(data, file)

    def change_state(self, *widgets):
        def changing_state_first(widgets):
            state = True
            for item_widget, badchangename, goodchangename in widgets:
                if item_widget.check():
                    change(item_widget, goodchangename)
                else:
                    change(item_widget, badchangename)
                    state = False
            if str(self.postioning_entry_repeat) != str(self.postioning_entry_password):
                state = False
                change(self.postioning_entry_repeat, badchangename)
                change(self.postioning_entry_password, badchangename)
            if state:
                self.create_new_user()

        def changing_state_back(widgets):
            for item_widget, oldname in widgets:
                change(item_widget, oldname)

        def change(item_widget, name):
            item_widget.entry.setObjectName(name)
            item_widget.entry.style().polish(item_widget.entry)

        changing_state_first(
            (
                (item_widget, badchangename, goodchangename)
                for item_widget, oldname, badchangename, goodchangename in widgets
            )
        )
        QTimer.singleShot(
            1000,
            lambda: changing_state_back(
                (
                    (item_widget, oldname)
                    for item_widget, oldname, badchangename, goodchangename in widgets
                )
            ),
        )

class SpotifyWindow:
    def __init__(self):
        self.window = QDialog()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    widget.setWindowTitle("SPOTIFY")
    app.setStyleSheet(open("style.css").read())
    win2 = SecondWindow()
    win = MainWindow()
    win3 = New_Account_Window()
    widget.addWidget(win2.window)
    widget.addWidget(win.window)
    widget.addWidget(win3.window)
    widget.setFixedHeight(500)
    widget.setFixedWidth(500)
    widget.show()
    sys.exit(app.exec())
