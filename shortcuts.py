from PyQt5.QtWidgets import QPushButton, QShortcut
from pynput import keyboard

import pyautogui
from PyQt5.QtCore import Qt, QUrl, QTime, QDir, QTimer
from PyQt5.QtGui import QIcon, QKeySequence, QCursor
import cv2
import os


class GlobalKeys:
    key_dictionary = {
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
    }
    GLOBAL_KEYS: bool = False
    on = list()

    def __init__(self, customvideoplayer, data):

        self.tab = customvideoplayer.tab
        self.videoplayer = customvideoplayer
        # self.global_button = QPushButton(self.tab)
        # self.global_button.setText("kliknij2")
        # self.global_button.clicked.connect(lambda: self.change_global())
        # self.global_button.setGeometry(500, 600, 60, 30)
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
        if GlobalKeys.GLOBAL_KEYS:
            GlobalKeys.GLOBAL_KEYS = False
            self.listener.stop()
            del self.listener
        else:
            GlobalKeys.GLOBAL_KEYS = True
            self.listener = keyboard.Listener(
                on_press=self.on_press_keyboard, on_release=self.on_release_keyboard
            )
            self.listener.start()

    def creating_short_cuts(self, data):

        shortcut = QShortcut(QKeySequence(Qt.Key_Right), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.forward(5) if not GlobalKeys.GLOBAL_KEYS else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Left), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.backward(5) if not GlobalKeys.GLOBAL_KEYS else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Up), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumeup(5) if not GlobalKeys.GLOBAL_KEYS else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Down), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumedown(5)
            if not GlobalKeys.GLOBAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Space), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.play() if not GlobalKeys.GLOBAL_KEYS else None
        )
        shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Up), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumeup(100)
            if not GlobalKeys.GLOBAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Down), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.volumedown(100)
            if not GlobalKeys.GLOBAL_KEYS
            else None
        )
        shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self.tab)
        shortcut.activated.connect(
            lambda: self.videoplayer.func_for_exit(data, next_window=True)
            if not GlobalKeys.GLOBAL_KEYS
            else None
        )

    def on_press_keyboard(self, key):
        if key not in GlobalKeys.on:
            GlobalKeys.on.append(key)

    def on_release_keyboard(self, key):
        try:
            GlobalKeys.key_dictionary[tuple(GlobalKeys.on)](self)
        except:
            ...
        finally:
            GlobalKeys.on.remove(key)
