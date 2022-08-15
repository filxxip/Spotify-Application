import json
from PyQt5.QtWidgets import QPushButton, QShortcut, QMessageBox
from pynput import keyboard
from .components import MyMsgBox

import pyautogui
from PyQt5.QtCore import Qt, QUrl, QTime, QDir, QTimer
from PyQt5.QtGui import QIcon, QKeySequence, QCursor
import cv2
import os

from pathlib import Path


class GlobalKeys:
    # key_dictionary = {
    #     tuple(
    #         [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.space]
    #     ): lambda self: self.videoplayer.play(),
    #     tuple(
    #         [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.left]
    #     ): lambda self: self.videoplayer.backward(5),
    #     tuple(
    #         [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.right]
    #     ): lambda self: self.videoplayer.forward(5),
    #     tuple(
    #         [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.up]
    #     ): lambda self: self.videoplayer.volumeup(5),
    #     tuple(
    #         [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.down]
    #     ): lambda self: self.videoplayer.volumedown(5),
    #     tuple(
    #         [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"),keyboard.KeyCode(char="z"), keyboard.Key.right]
    #     ): lambda self: self.videoplayer.next_video_button.click(),
    #     tuple(
    #         [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"),keyboard.KeyCode(char="z"), keyboard.Key.left]
    #     ): lambda self: self.videoplayer.previous_video_button.click(),
    # }

    def __init__(self, customvideoplayer, data, start=False):
        self.LOCAL_KEYS = True
        self.GLOBAL_KEYS = False
        self.on = list()
        self.master = customvideoplayer.window
        self.tab = customvideoplayer.tab
        self.videoplayer = customvideoplayer
        self.creating_global_shortcuts()
        # self.global_button = QPushButton(self.tab)
        # self.global_button.setText("kliknij2")
        # self.global_button.clicked.connect(lambda: self.change_global())
        # self.global_button.setGeometry(500, 600, 60, 30)
        if start:
            self.change_global()
        self.creating_short_cuts(data)
        self.removing_shortcuts()

    def removing_shortcuts(self):
        QShortcut(
            QKeySequence(Qt.ControlModifier + Qt.Key_Space), self.tab
        ).activated.connect(lambda: None)
        QShortcut(
            QKeySequence(Qt.ControlModifier + Qt.Key_Left), self.tab
        ).activated.connect(lambda: None)
        QShortcut(
            QKeySequence(Qt.ControlModifier + Qt.Key_Right), self.tab
        ).activated.connect(lambda: None)
        QShortcut(
            QKeySequence(Qt.ControlModifier + Qt.Key_Down), self.tab
        ).activated.connect(lambda: None)
        QShortcut(
            QKeySequence(Qt.ControlModifier + Qt.Key_Up), self.tab
        ).activated.connect(lambda: None)

    def change_global(self):
        if self.GLOBAL_KEYS:
            self.GLOBAL_KEYS = False
            self.listener.stop()
            del self.listener
        else:
            self.GLOBAL_KEYS = True
            self.listener = keyboard.Listener(
                on_press=self.on_press_keyboard, on_release=self.on_release_keyboard
            )
            self.listener.start()

    def creating_global_shortcuts(self):
        self.key_dictionary = {
            tuple(
                [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.space]
            ): lambda self: self.videoplayer.play(),
            tuple(
                [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.left]
            ): lambda self: self.videoplayer.backward(5),
            tuple(
                [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.right]
            ): lambda self: self.videoplayer.forward(5),
            tuple(
                [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.up]
            ): lambda self: self.videoplayer.volumeup(5),
            tuple(
                [keyboard.Key.ctrl_l, keyboard.KeyCode(char="<"), keyboard.Key.down]
            ): lambda self: self.videoplayer.volumedown(5),
            tuple(
                [
                    keyboard.Key.ctrl_l,
                    keyboard.KeyCode(char="<"),
                    keyboard.KeyCode(char="z"),
                    keyboard.Key.right,
                ]
            ): lambda self: self.videoplayer.next_video_button.click(),
            tuple(
                [
                    keyboard.Key.ctrl_l,
                    keyboard.KeyCode(char="<"),
                    keyboard.KeyCode(char="z"),
                    keyboard.Key.left,
                ]
            ): lambda self: self.videoplayer.previous_video_button.click(),
        }

    def creating_short_cuts(self, data):

        shortcut = QShortcut(QKeySequence(Qt.Key_Right), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.forward(5)
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None
        )
        import __main__

        with open(
            f"{Path(__main__.__file__).parent.__str__()}/json_files/data_main_window.json"
        ) as file:
            data2 = json.load(file)
        shortcut = QShortcut(QKeySequence(Qt.Key_I), self.tab)
        shortcut.activated.connect(
            lambda: MyMsgBox(
                **data2["information"], OK=[QMessageBox.YesRole, lambda: None]
            )
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else MyMsgBox(
                **data2["information2"], OK=[QMessageBox.YesRole, lambda: None]
            )
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Left), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.backward(5)
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Up), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumeup(5)
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Down), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumedown(5)
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Space), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.play()
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None  # cos nie tak z local
        )
        shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Up), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumeup(100)
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Down), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumedown(100)
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Right), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.next_video_button.click()
            if (not self.GLOBAL_KEYS and self.LOCAL_KEYS)
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Left), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.previous_video_button.click()
            if not self.GLOBAL_KEYS and self.LOCAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self.master)
        shortcut.activated.connect(
            lambda: self.videoplayer.func_for_exit(data, next_window=True)
            if not self.GLOBAL_KEYS
            else None
        )

    def on_press_keyboard(self, key):
        if key not in self.on:
            self.on.append(key)

    def on_release_keyboard(self, key):
        try:
            self.key_dictionary[tuple(self.on)](self)
        except:
            ...
        finally:
            self.on.remove(key)
