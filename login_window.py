from components import MyError
import sys
from PyQt5.QtCore import Qt, QSize, QEvent, QTimer
from PyQt5.QtWidgets import QMessageBox, QDialog
import json

from components import (
    Label_Entry_Box,
    MyButtonwithImage,
    MyCheckBox,
    MyError,
    MyLabelwithImage,
    MyMsgBox,
    Mybuttonwithtext,
    State,
)
from blocking_decorator import blocked_button

# from open_window import OpenWindow
# from spotify_window import SpotifyWindow


class LoginWindow:
    dimensions = (500, 500)

    def __init__(self, master):
        self.master = master
        self.window = QDialog()
        self.window.eventFilter = self.eventFilter
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

    def entry_setter(self):
        with open("json_files/data.json") as file:
            data = json.load(file)

        self.login.entry = data["remembered_data"]["login"]
        self.password.entry = data["remembered_data"]["password"]
        if self.login and self.password:
            self.checkbox.state = True

    def func_for_exit(self, data):
        from open_window import OpenWindow

        MyMsgBox(
            **data,
            Yeah=[QMessageBox.YesRole, lambda: self.master.set_widget(OpenWindow)],
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

    @blocked_button("submit_button.button", 3)
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
                        from spotify_window import SpotifyWindow

                        MyMsgBox(
                            **data_message_green,
                            OK=[
                                QMessageBox.AcceptRole,
                                lambda: self.master.add_and_set(SpotifyWindow),
                            ],
                        )
                    else:
                        self.change_state()
                        raise MyError("wrong password")
                else:
                    self.change_state()
                    raise MyError("login undefined")
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
