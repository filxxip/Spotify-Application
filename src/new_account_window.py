import os
from PyQt5.QtCore import Qt, QSize, QEvent, QTimer
from PyQt5.QtWidgets import (
    QMessageBox,
    QDialog,
)
import json
from pathlib import Path
from .components import (
    Label_Entry_Box_Age,
    Label_Entry_Box_Country,
    Label_Entry_Box_Gender,
    Label_Entry_Box_Login,
    Label_Entry_Box_Name,
    Label_Entry_Box_Nationality,
    Label_Entry_Box_Password,
    Label_Entry_Box_Surname,
    MyButtonwithImage,
    MyLabelwithImage,
    MyMsgBox,
    Mybuttonwithtext,
)
from .blocking_decorator import blocked_button
import __main__


class New_Account_Window:
    dimensions = (500, 500)

    def __init__(self, master):
        self.master = master
        self.window = QDialog()
        self.window.eventFilter = self.eventFilter
        with open(
            rf"{Path(__main__.__file__).parent.__str__()}/json_files/new_account_window.json"
        ) as file:
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
        from open_window import OpenWindow

        MyMsgBox(
            **data,
            Yeah=[QMessageBox.YesRole, lambda: self.master.set_widget(OpenWindow)],
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
        with open(
            rf"{Path(__main__.__file__).parent.__str__()}/json_files/new_account_window.json"
        ) as file:
            data = json.load(file)["messagebox_new_account"]
        from open_window import OpenWindow

        MyMsgBox(
            **data,
            Great=[QMessageBox.YesRole, lambda: self.master.set_widget(OpenWindow)],
        )
        with open(
            rf"{Path(__main__.__file__).parent.__str__()}/json_files/file.json"
        ) as file:
            data = json.load(file)
        data[self.postioning_entry_login.__str__()] = {
            "name": self.postioning_entry_name.__str__(),
            "surname": self.postioning_entry_surname.__str__(),
            "password": self.postioning_entry_password.__str__(),
            "age": self.postioning_entry_age.__str__(),
            "country": self.postioning_entry_coutry.__str__(),
            "nationality": self.postioning_entry_nationality.__str__(),
            "gender": self.postioning_entry_gender.__str__(),
            "songs": [],
        }
        with open(
            rf"{Path(__main__.__file__).parent.__str__()}/json_files/file.json", "w"
        ) as file:
            json.dump(data, file)

    def change_state(self, *widgets):
        def changing_state_first(widgets):
            state = True
            incorrects = []
            for item_widget, badchangename, goodchangename in widgets:
                if item_widget.check():
                    change(item_widget, goodchangename)
                else:
                    change(item_widget, badchangename)
                    incorrects.append(item_widget)
                    state = False
            if str(self.postioning_entry_repeat) != str(self.postioning_entry_password):
                state = False
                change(self.postioning_entry_repeat, badchangename)
                change(self.postioning_entry_password, badchangename)
            if state:
                self.create_new_user()
            else:
                with open(
                    rf"{Path(__main__.__file__).parent.__str__()}/json_files/new_account_window.json"
                ) as file:
                    data = json.load(file)
                text = ""
                for index, cls in enumerate(incorrects):
                    text += f"{index+1} -> {data[cls.__class__.__name__]}\n"
                MyMsgBox(
                    title="Error in creating new account.",
                    text=text,
                    name="messagebox_red",
                    icon="images/spotifyimg.png",
                    OK=[QMessageBox.YesRole, lambda: None],
                )
                incorrects.clear()

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
