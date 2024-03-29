import enum
import os
import time
from PyQt5.QtWidgets import (
    QMessageBox,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QStyle,
    QFileDialog,
    QDialog,
)

import pyautogui
import json
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from .components import MyButtonwithImage, MyLabelwithImage, MyMsgBox
from PyQt5.QtCore import (
    Qt,
    QUrl,
    QTime,
    QDir,
    QTimer,
    QObject,
    pyqtSignal,
    QSize,
    QThread,
)
from PyQt5.QtGui import QIcon, QCursor
import cv2
from .shortcuts import GlobalKeys
from PyQt5.QtTest import QTest


class Status(enum.Enum):
    FULL = enum.auto()
    SMALL = enum.auto()
    FULLSIZE = enum.auto()


class MySingal(QObject):
    signal = pyqtSignal(bool, int)


import __main__


class ImageChangableButton:
    def __init__(self, image1, image2, function, current_status, size=(30, 30)):
        self.signal = MySingal()
        self.button = QPushButton()
        self.func = function
        self.button.setIconSize(QSize(*size))
        self.image1 = QIcon(f"{Path(__main__.__file__).parent.__str__()}/{image1}")
        self.image2 = QIcon(f"{Path(__main__.__file__).parent.__str__()}/{image2}")
        self.button.setCursor(Qt.OpenHandCursor)
        if current_status:
            self.setIcon(self.image2)
        else:
            self.setIcon(self.image1)
        self.button.setObjectName("image_with_background")
        self.button.clicked.connect(self.command)
        self.button.enterEvent = lambda event: self.eventcommand(event)
        self.button.leaveEvent = lambda event: self.eventcommand(event)

    def eventcommand(self, event):
        if self.currenticon == self.image1:
            self.setIcon(self.image2)
        elif self.currenticon == self.image2:
            self.setIcon(self.image1)

    def setIcon(self, icon):
        self.button.setIcon(icon)
        self.currenticon = icon

    def change_event(self, event):
        self.button.leaveEvent = lambda event: self.eventcommand(event)

    def command(self):
        if self.func():
            self.setIcon(self.image2)
            self.button.leaveEvent = lambda event: self.change_event(event)
        else:
            self.setIcon(self.image1)
            self.button.leaveEvent = lambda event: self.change_event(event)


import datetime


class GUIThread(QThread):
    seton = pyqtSignal()
    setoff = pyqtSignal()

    def __init__(self, function):
        # self.signal = MySignal6()
        self.function = function
        super().__init__()

    def run(self):
        while True:
            time.sleep(0.25)
            if self.function() == Status.FULLSIZE:
                if pyautogui.position().y > 1000:
                    self.seton.emit()
                else:
                    self.setoff.emit()
            else:
                break


class ClickThred(QThread):
    long_process = pyqtSignal()
    short_process = pyqtSignal()
    change_color = pyqtSignal(int)

    def __init__(self, buttoncheck, number_states, seconds=1, miliseconds=0):
        self.buttoncheck = buttoncheck
        self.number_states = number_states
        self.seconds = seconds
        self.miliseconds = miliseconds
        super().__init__()

    def run(self):
        time = datetime.datetime.now()
        deltatime = datetime.timedelta(
            seconds=self.seconds, milliseconds=self.miliseconds
        )
        basic = 0
        deltastate = self.seconds * 1000 + self.miliseconds
        deltastate = int(deltastate / self.number_states)
        while self.buttoncheck():
            time2 = datetime.datetime.now()
            diff = time2 - time
            if diff > datetime.timedelta(milliseconds=deltastate * basic):
                self.change_color.emit(basic)
                basic += 1
            if diff > deltatime:
                self.long_process.emit()
                self.change_color.emit(0)
                return
        time2 = datetime.datetime.now()
        self.short_process.emit()
        self.change_color.emit(0)


class CustomizeButtonWithImage(MyButtonwithImage):
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
        **restimages,
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
            image,
            name2,
            image2,
        )
        self.allimages = [QIcon(f"{Path(__main__.__file__).parent.__str__()}/{image}")]
        for image in restimages.values():
            self.allimages.append(
                QIcon(f"{Path(__main__.__file__).parent.__str__()}/{image}")
            )
        self.button.setIcon(self.allimages[0])

    def change_state(self, index):
        self.button.setIcon(self.allimages[index])


from pathlib import Path


class CloseSignal(QObject):
    signal = pyqtSignal()


class CustomVideoPlayer:
    marg = 10, 30, 10, 55

    def __init__(self, master, window, tab, removing_function, seeing_function, layout):
        self.video_name = None
        self.closesignal = CloseSignal()
        self.autoplay = True
        self.status = Status.FULL
        self.signal = MySingal()
        self.master = master
        self.window = window
        self.remove_func = removing_function
        self.see_func = seeing_function
        self.tab: QDialog = tab
        self.main_layout = layout
        with open(
            rf"{Path(__main__.__file__).parent.__str__()}/json_files/data_spotify_window.json"
        ) as data:
            data = json.load(data)
        self.master.widget.closeEvent = lambda event: self.exit_func(event)
        self.label = MyLabelwithImage(self.tab, **data["label"])
        self.global_keys = GlobalKeys(
            self, data["message_box_cancel_window"], start=False
        )
        self.creation_of_mediaplayer()
        self.creation_of_layout()
        self.end_time = 0

        def f():
            self.tab.mouseMoveEvent = lambda event: self.moving_window(event)
            self.videoWidget.mousePressEvent = lambda event: self.func1(event)
            self.videoWidget.mouseReleaseEvent = lambda event: self.func2(event)

        def f2():
            self.tab.mouseMoveEvent = lambda event: None
            self.videoWidget.mousePressEvent = lambda event: None
            self.videoWidget.mouseReleaseEvent = lambda event: None

        QTimer.singleShot(1, f)
        QTimer.singleShot(1, f2)
        QTimer.singleShot(22, lambda: self.tab.setWindowFlag(Qt.WindowStaysOnTopHint))
        self.master.widget.closeEvent = lambda event: self.exit_func(event)
        self.videoWidget.mouseDoubleClickEvent = lambda event: self.change_size2(event)
        self.videoWidget.hide()
        self.status_play_bar(False)

    def stopfunction(self, name):
        if self.video_name:
            if name == self.video_name.split("/")[-1]:
                self.set_spotife_title()

    def autoplay_function(self):
        if self.autoplay:
            self.autoplay = False
        else:
            self.autoplay = True
        return self.autoplay

    def global_keys_function(self):
        self.global_keys.change_global()
        return self.global_keys.GLOBAL_KEYS

    def creation_of_mediaplayer(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.media_state_change)
        self.mediaPlayer.positionChanged.connect(self.slider_position_change)
        self.mediaPlayer.durationChanged.connect(self.slider_duration_change)
        self.mediaPlayer.volumeChanged.connect(self.setSound)

    def creating_layout(self, *positions):
        self.horizontallayout = QHBoxLayout()
        self.horizontallayout.addWidget(self.playbutton, 1)
        self.horizontallayout.addWidget(self.previous_video_button, 1)
        self.horizontallayout.addWidget(self.next_video_button, 1)
        self.horizontallayout.addWidget(self.autoplay_button.button, 1)
        self.horizontallayout.addWidget(self.global_keys_button.button, 1)
        self.horizontallayout.addWidget(self.soundbutton, 1)
        self.horizontallayout.addWidget(self.slider_sound, 10)
        self.horizontallayout.addWidget(self.start_time_lbl)
        self.horizontallayout.addWidget(self.slider, 70)
        self.horizontallayout.addWidget(self.end_time_lbl)
        self.horizontallayout.addWidget(self.size_button.button, 1)
        # self.horizontallayout.addWidget(self.remmovebutton, 1)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(self.label.label)
        self.layout.addLayout(self.horizontallayout)
        # self.tab.setLayout(layout)

    def thread_function(self):
        self.mythread = ClickThred(
            self.size_button.button.isDown,
            len(self.size_button.allimages),
            seconds=0,
            miliseconds=300,
        )
        self.mythread.start()
        if self.status == Status.FULL:
            try:
                self.mythread.long_process.disconnect()
            except:
                pass
            self.mythread.long_process.connect(lambda: self.full_screen())
        elif self.status == Status.FULLSIZE:
            try:
                self.mythread.long_process.disconnect()
            except:
                pass
            self.mythread.long_process.connect(
                lambda: self.change_size(change_position=False)
            )  # cos zeby ladnie sie wgralo
        self.mythread.short_process.connect(lambda: self.change_size2())
        self.mythread.change_color.connect(lambda index: self.change_color(index))

    def change_color(self, index):
        try:
            self.size_button.change_state(index)
        except IndexError:
            pass

    def creation_of_layout(self):
        with open(
            rf"{Path(__main__.__file__).parent.__str__()}/json_files/data_spotify_window.json"
        ) as data:
            data = json.load(data)
        self.size_button = CustomizeButtonWithImage(
            self.tab,
            **data["small_size"],
            function_pressed=lambda: self.thread_function(),
        )
        self.size_button.button.setMaximumSize(20, 20)
        self.playbutton = QPushButton()
        self.playbutton.setIcon(self.tab.style().standardIcon(QStyle.SP_MediaPlay))
        self.playbutton.clicked.connect(self.play)
        # self.remmovebutton = QPushButton()
        # removeicon = QIcon(rf"{Path(__main__.__file__).parent.__str__()}/images/delete.png")
        # self.remmovebutton.setIcon(removeicon)
        # self.remmovebutton.setIconSize(QSize(20, 20))
        # self.remmovebutton.setMaximumSize(20, 20)
        # self.remmovebutton.clicked.connect(self.play)
        self.soundbutton = QPushButton()
        self.soundbutton.setObjectName("aaa")
        self.playbutton.setObjectName("aaa")
        # self.remmovebutton.setObjectName("aaa")
        self.soundbutton.setIcon(self.tab.style().standardIcon(QStyle.SP_MediaVolume))
        self.soundbutton.clicked.connect(self.change_sound)
        self.previous_video_button = QPushButton()
        self.previous_video_button.setObjectName("aaa")
        self.previous_video_button.clicked.connect(
            lambda: self.signal.signal.emit(False, self.slider.sliderPosition())
        )
        self.previous_video_button.setIcon(
            self.tab.style().standardIcon(QStyle.SP_MediaSeekBackward)
        )
        self.next_video_button = QPushButton()
        self.next_video_button.setObjectName("aaa")
        self.next_video_button.clicked.connect(
            lambda: self.signal.signal.emit(True, self.slider.sliderPosition())
        )
        self.next_video_button.setIcon(
            self.tab.style().standardIcon(QStyle.SP_MediaSeekForward)
        )
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.setPosition)
        self.slider.setCursor(QCursor(Qt.UpArrowCursor))
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider_sound = QSlider(Qt.Horizontal)
        self.slider_sound.sliderMoved.connect(self.setSound)
        self.slider_sound.setSliderPosition(50)
        self.slider_sound.setCursor(QCursor(Qt.UpArrowCursor))
        self.mediaPlayer.setVolume(50)
        self.start_time_lbl = QLabel("00:00:00")
        self.end_time_lbl = QLabel("00:00:00")
        self.autoplay_button = ImageChangableButton(
            "images/autoplay-off",
            "images/autoplay-on",
            self.autoplay_function,
            self.autoplay,
        )
        self.global_keys_button = ImageChangableButton(
            "images/globaloff",
            "images/globalon",
            self.global_keys_function,
            self.global_keys.GLOBAL_KEYS,
            size=(24, 24),
        )
        self.creating_layout(*CustomVideoPlayer.marg)

    def full_screen(self):
        screen = self.master.master.primaryScreen()
        screensize = screen.size()
        self.status = Status.FULLSIZE
        self.master.widget.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.master.widget.setWindowFlag(Qt.FramelessWindowHint)
        QTimer.singleShot(20, lambda: self.master.widget.show())
        self.remove_func()
        self.master.set_dimentions(screensize.width(), screensize.height())
        self.master.widget.setWindowState(Qt.WindowFullScreen)
        self.master.widget.setGeometry(0, 0, self.master.width, self.master.height)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.videoWidget.mouseDoubleClickEvent = lambda event: self.change_size(event)
        self.status_play_bar(False)
        QTest.mousePress(self.tab, Qt.LeftButton)
        self.videoWidget.setMouseTracking(True)
        self.master.widget.setWindowFlags(
            self.master.widget.windowFlags() & ~Qt.WindowStaysOnTopHint
        )
        self.mythread = GUIThread(self.get_status)
        self.mythread.start()
        self.mythread.seton.connect(
            lambda: [
                self.status_play_bar(True),
                self.horizontallayout.setContentsMargins(50, 0, 50, 5),
            ]
        )
        self.mythread.setoff.connect(
            lambda: [
                self.status_play_bar(False),
                self.horizontallayout.setContentsMargins(0, 0, 0, 0),
            ]
        )

    def get_status(self):
        return self.status

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.tab, "Open Movie", QDir.homePath() + "/filip/Documents/qt-learning"
        )
        if filename != "":
            self.open_movie(filename)
            self.set_spotife_title(False)

    def func1(self, event):
        if event.button() == Qt.LeftButton:
            self.tab.mouseMoveEvent = lambda event: self.moving_window(event)

    def func2(self, event):
        if event.button() == Qt.LeftButton:
            self.tab.mouseMoveEvent = lambda event: None

    def moving_window(self, event):
        vid = cv2.VideoCapture(self.video_name)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.master.widget.setGeometry(
            event.globalPos().x() - int(width / 10),
            event.globalPos().y() - int(height / 10),
            self.master.width,
            self.master.height,
        )

    def change_size2(self, event=None, change_position=True):
        if not event or event.button() == Qt.LeftButton:
            self.horizontallayout.setContentsMargins(0, 0, 0, 0)
            self.status = Status.SMALL
            self.videoWidget.setCursor(Qt.DragMoveCursor)
            self.videoWidget.mousePressEvent = lambda event: self.func1(event)
            self.videoWidget.mouseReleaseEvent = lambda event: self.func2(event)
            x, y = pyautogui.position()
            vid = cv2.VideoCapture(self.video_name)
            height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            # self.tabbar.hide()
            self.master.widget.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.master.widget.setWindowFlag(Qt.FramelessWindowHint)
            QTimer.singleShot(20, lambda: self.master.widget.show())
            self.master.widget.show()  # wyrzuca flagi
            self.status_play_bar(False)
            self.remove_func()
            self.master.set_dimentions(
                round(width / 5), round(height / 5)
            )  # setting heigth and width
            if not event:  # setting position
                if change_position:
                    self.master.widget.setGeometry(
                        x
                        - int(self.videoWidget.width() / 2)
                        - 3 * int(self.master.width / 2),
                        y
                        - int(self.videoWidget.height() / 2)
                        - 3 * int(self.master.height / 2),
                        self.master.width,
                        self.master.height,
                    )
                else:
                    self.master.widget.setGeometry(
                        self.master.widget.geometry().x(),
                        self.master.widget.geometry().y(),
                        self.master.width,
                        self.master.height,
                    )
            if event:  # setting position
                self.master.widget.setGeometry(
                    x - int(width / 10),
                    y - int(height / 10),
                    self.master.width,
                    self.master.height,
                )
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            # self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.tab.setMouseTracking(True)
            self.tab.mouseMoveEvent = lambda event: self.moving_window(event)
            self.videoWidget.mouseDoubleClickEvent = lambda event: self.change_size(
                event
            )
            self.master.widget.setWindowOpacity(0.6)

    def change_size(self, event=None, change_position=True):
        if not event or event.button() == Qt.LeftButton:
            self.horizontallayout.setContentsMargins(0, 0, 0, 0)
            self.status = Status.FULL
            self.videoWidget.mousePressEvent = lambda event: None
            self.videoWidget.mouseReleaseEvent = lambda event: None
            x, y = pyautogui.position()
            self.videoWidget.windowState()
            self.master.widget.setWindowState(
                self.master.widget.windowState() & ~Qt.WindowFullScreen
            )
            self.master.widget.setWindowFlags(
                self.master.widget.windowFlags() & ~Qt.FramelessWindowHint
            )
            self.master.widget.setWindowFlags(
                self.master.widget.windowFlags() & ~Qt.WindowStaysOnTopHint
            )
            # self.master.widget.show()
            self.see_func()
            # self.tabbar.show()
            self.status_play_bar(True)
            self.master.set_dimentions(*self.window.dimensions)
            if change_position:
                self.master.widget.setGeometry(
                    x - int(self.master.width / 2),
                    y - int(self.master.height / 2),
                    self.master.width,
                    self.master.height,
                )
            else:
                self.master.widget.setGeometry(
                    x, y, self.master.width, self.master.height
                )
            self.master.widget.show()
            self.main_layout.setContentsMargins(*CustomVideoPlayer.marg)
            self.layout.setContentsMargins(20, 0, 20, 0)
            self.tab.mouseMoveEvent = lambda event: None
            self.tab.setMouseTracking(False)
            self.videoWidget.mouseDoubleClickEvent = lambda event: self.change_size2(
                event
            )
            self.master.widget.setWindowOpacity(1)

    def forward(self, value):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + value * 1000)
        if self.mediaPlayer.position() > self.end_time:
            self.mediaPlayer.setPosition(self.end_time)

    def backward(self, value):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - value * 1000)
        if self.mediaPlayer.position() < 0:
            self.mediaPlayer.setPosition(0)

    def volumeup(self, value):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + value)
        self.slider_sound.setValue(self.slider_sound.value() + value)

    def volumedown(self, value):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - value)
        self.slider_sound.setValue(self.slider_sound.value() - value)

    def status_play_bar(self, status: bool):
        # self.videoWidget.setVisible(status)
        self.playbutton.setVisible(status)
        self.next_video_button.setVisible(status)
        self.previous_video_button.setVisible(status)
        self.soundbutton.setVisible(status)
        self.slider_sound.setVisible(status)
        self.slider.setVisible(status)
        self.start_time_lbl.setVisible(status)
        self.end_time_lbl.setVisible(status)
        self.size_button.button.setVisible(status)
        self.autoplay_button.button.setVisible(status)
        self.global_keys_button.button.setVisible(status)
        # self.remmovebutton.setVisible(status)

    def set_spotife_title(self, status=True):
        if status:
            if self.status == Status.SMALL or self.status == Status.FULLSIZE:
                self.change_size()
            self.global_keys.LOCAL_KEYS = False
            self.label.label.show()
            self.videoWidget.hide()
            self.status_play_bar(False)
            self.mediaPlayer.stop()

        else:
            self.global_keys.LOCAL_KEYS = True
            self.label.label.hide()
            self.videoWidget.show()
            self.status_play_bar(True)

    def change_sound(self):
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            self.soundbutton.setIcon(
                self.tab.style().standardIcon(QStyle.SP_MediaVolume)
            )
        else:
            self.mediaPlayer.setMuted(True)
            self.soundbutton.setIcon(
                self.tab.style().standardIcon(QStyle.SP_MediaVolumeMuted)
            )

    def open_movie(self, name, play=True):
        if name:
            if self.videoWidget.isHidden():
                self.set_spotife_title(False)
            self.video_name = name
            media = QMediaContent(QUrl.fromLocalFile(f"{name}"))
            self.mediaPlayer.setMedia(media)
            # QTimer.singleShot(20, self.playbutton.click)
            # if self.status == Status.SMALL:
            #     self.change_size2(change_position=False)
            if play:
                QTimer.singleShot(20, self.playbutton.click)
        else:
            self.mediaPlayer.stop()
            self.set_spotife_title()

    def slider_position_change(self, position):
        if (position < self.end_time) or self.end_time == 0 or not self.autoplay:
            self.slider.setValue(position)
            time = QTime(0, 0, 0, 0).addMSecs(self.mediaPlayer.position())
            self.start_time_lbl.setText(time.toString())
            if position == self.end_time and self.end_time != 0:
                QTest.mouseRelease(self.slider, Qt.LeftButton)
                self.open_movie(self.video_name, play=False)
        else:
            QTest.mouseRelease(self.slider, Qt.LeftButton)
            self.signal.signal.emit(self.video_name, True, self.slider.sliderPosition())

    def slider_duration_change(self, position):
        self.end_time = position
        self.slider.setRange(0, position)
        time = QTime(0, 0, 0, 0).addMSecs(self.mediaPlayer.duration())
        self.end_time_lbl.setText(time.toString())

    def media_state_change(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playbutton.setIcon(self.tab.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playbutton.setIcon(self.tab.style().standardIcon(QStyle.SP_MediaPlay))

    def play(self):  # work
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def setSound(self, position):
        self.mediaPlayer.setVolume(position)
        if position == 0:
            self.soundbutton.setIcon(
                self.tab.style().standardIcon(QStyle.SP_MediaVolumeMuted)
            )
        else:
            self.mediaPlayer.setMuted(False)
            self.soundbutton.setIcon(
                self.tab.style().standardIcon(QStyle.SP_MediaVolume)
            )

    def exit_func(self, event=None, next_window=False):
        from .open_window import OpenWindow

        if self.__dict__.get("mediaPlayer"):
            self.mediaPlayer.stop()
        if next_window:
            self.master.set_widget(OpenWindow)
        else:
            if self.__dict__.get("mediaPlayer"):
                del self.mediaPlayer
            del self.master.windows["SpotifyWindow"]
            exit()
        try:

            self.global_keys.listener.stop()
        except AttributeError:
            pass
        finally:
            self.set_spotife_title(True)
            self.closesignal.signal.emit()

    def func_for_exit(self, data, next_window=True):
        MyMsgBox(
            **data,
            Yeah=[
                QMessageBox.YesRole,
                lambda: self.exit_func(next_window, next_window=next_window),
            ],
            Nope=[QMessageBox.NoRole, lambda: None],
        )
