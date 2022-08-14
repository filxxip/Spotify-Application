import os
from PyQt5.QtWidgets import QDialog, QMessageBox
import json
from .components import (
    MyButtonwithImage,
    MyLabelwithImage,
    MyLabelwithText,
    MyMsgBox,
)
from pathlib import Path
from PyQt5.QtCore import Qt, QSize, QEvent, QTimer
import __main__

# from login_window import LoginWindow
# from new_account_window import New_Account_Window
class OpenWindow:
    dimensions = (500, 500)

    def __init__(self, master):
        from .login_window import LoginWindow
        from .new_account_window import New_Account_Window

        self.master = master
        self.window = QDialog()
        self.window.eventFilter = self.eventFilter
        with open(
            rf"{Path(__main__.__file__).parent.__str__()}/json_files/data_second_window.json"
        ) as data:
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
                self.master.add_and_set(LoginWindow),
                self.new_account.button.setCheckable(False),
            ],
        )
        self.new_account = MyButtonwithImage(
            self.window,
            **data["password_button"],
            function_clicked=lambda: [
                self.master.add_and_set(New_Account_Window),
                self.new_account.button.setCheckable(False),
            ],
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
            Yeah=[QMessageBox.YesRole, lambda: exit()],
            Nope=[QMessageBox.NoRole, lambda: None],
        )
