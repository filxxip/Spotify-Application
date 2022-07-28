import enum
from PyQt5.QtWidgets import (
    QMessageBox,
    QDialog,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QStyle,
    QFileDialog,
    QAction,
    QLineEdit,
    QShortcut,
)
from moviepy.editor import VideoFileClip
import pyautogui
import json
from PyQt5.QtMultimedia import (
    QMediaContent,
    QMediaPlayer,
    QMediaMetaData,
    QMediaPlaylist,
)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from base_component import BaseForAll
from components import MyButtonwithImage, MyLabel, MyMsgBox, Mybuttonwithtext
from PyQt5.QtCore import Qt, QUrl, QTime, QPoint, QSize, QDir
from PyQt5.QtGui import QIcon, QKeySequence, QCursor
import cv2
import os


class MyTab:
    def __init__(self, master, window, title):
        self.master: BaseForAll = master
        self.window = window
        self.tab = QWidget()
        self.tab.setObjectName("tabwidget")
        self.window.addTab(self.tab, title)

    @property
    def tabbar(self):
        return self.window.tabBar()


class FirstTab(MyTab):
    marg = (50, 20, 50, 400)

    def __init__(self, master, window, title):
        super().__init__(master, window, title)
        with open("json_files/data_spotify_window.json") as data:
            data = json.load(data)
        self.master.widget.closeEvent = lambda event: self.exit_func(event)
        self.cancel_button = MyButtonwithImage(
            self.tab,
            function_clicked=lambda: self.func_for_exit(
                data["message_box_cancel_window"]
            ),
            **data["cancel_button"],
        )

        self.clickable_button = QPushButton(self.tab)
        self.clickable_button.setText("kliknij")
        self.clickable_button.clicked.connect(
            lambda: self.open_file(
                # "/home/filip/Documents/qt-learning/Coldplay X Selena Gomez - Let Somebody Go (Official Video).mp4"
            )
        )
        self.creation_of_mediaplayer()
        self.creation_of_layout()
        self.creating_short_cuts()
        self.size_button.button.click()
        self.videoWidget.mousePressEvent = lambda event: None
        self.videoWidget.mouseReleaseEvent = lambda event: None
        self.videoWidget.mouseDoubleClickEvent = lambda event : self.change_size2(event)
        x, y = pyautogui.position()
        self.master.widget.setWindowFlags(
            self.master.widget.windowFlags() & ~Qt.FramelessWindowHint
        )
        self.master.widget.setWindowFlags(
            self.master.widget.windowFlags() & ~Qt.WindowStaysOnTopHint
        )
        self.master.widget.show()
        self.tabbar.show()
        self.status_play_bar(True)
        self.master.set_dimentions(*self.window.dimensions)
        self.master.widget.setGeometry(
            x - int(self.master.width / 2),
            y - int(self.master.height / 2),
            self.master.width,
            self.master.height,
        )
        self.layout.setContentsMargins(*FirstTab.marg)
        self.tab.mouseMoveEvent = lambda event: None
        self.tab.setMouseTracking(False)

    def creation_of_mediaplayer(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.videoWidget = QVideoWidget()
        # mp4 = "/home/filip/Documents/qt-learning/songs/Coldplay - Biutyful (Official Video).mp4"
        # mp3 = "/home/filip/Documents/qt-learning/songs/Coldplay - Biutyful (Official Video).mp3"
        # videoclip =  VideoFileClip(mp4)
        # audioclip = videoclip.audio
        # audioclip.write_audiofile(mp3)
        # audioclip.close()
        # videoclip.close()
        # self.video_name = '/home/filip/Documents/qt-learning/songs/Coldplay - Biutyful (Official Video).mp3'
        # media = QMediaContent(QUrl.fromLocalFile('/home/filip/Documents/qt-learning/songs/Coldplay - Biutyful (Official Video).mp3'))
        # self.mediaPlayer.setMedia(media)
        # self.videoWidget.addMedia(QMediaContent(QUrl('/home/filip/Documents/qt-learning/songs/Coldplay - Biutyful (Official Video).mp3')))

        
        self.videoWidget = QVideoWidget()
        self.open_movie(
            "/home/filip/Documents/qt-learning/songs/Coldplay X Selena Gomez - Let Somebody Go (Official Video).mp4"
        )
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.media_state_change)
        self.mediaPlayer.positionChanged.connect(self.slider_position_change)
        self.mediaPlayer.durationChanged.connect(self.slider_duration_change)
        self.mediaPlayer.volumeChanged.connect(self.setSound)

    def creation_of_layout(self):
        with open("json_files/data_spotify_window.json") as data:
            data = json.load(data)
        self.size_button = MyButtonwithImage(
            self.tab, **data["small_size"], function_clicked=lambda: self.change_size2()
        )
        self.size_button.button.setMaximumSize(20, 20)
        self.playbutton = QPushButton()
        self.playbutton.setIcon(self.tab.style().standardIcon(QStyle.SP_MediaPlay))
        self.playbutton.clicked.connect(self.play)
        self.soundbutton = QPushButton()
        self.soundbutton.setIcon(self.tab.style().standardIcon(QStyle.SP_MediaVolume))
        self.soundbutton.clicked.connect(self.change_sound)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.setPosition)
        self.slider.setCursor(QCursor(Qt.UpArrowCursor))

        self.slider_sound = QSlider(Qt.Horizontal)
        self.slider_sound.sliderMoved.connect(self.setSound)

        self.slider_sound.setSliderPosition(50)
        self.mediaPlayer.setVolume(50)

        self.start_time_lbl = QLabel("00:00:00")
        self.end_time_lbl = QLabel("00:00:00")
        self.creating_layout(*FirstTab.marg)
        # self.layout.setContentsMargins(*FirstTab.marg)
    def open_file(self):
        files = os.listdir('/home/filip/Documents/qt-learning/songs')
        print(files)
        filename, _ = QFileDialog.getOpenFileName(self.tab, "Open Movie", QDir.homePath() + "/filip/Documents/qt-learning")
        if filename!="":
            self.open_movie(filename)
    def func1(self, event):
        self.tab.mouseMoveEvent = lambda event: self.moving_window(event)

    def func2(self, event):
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

    def change_size2(self, event = None):
        self.videoWidget.mousePressEvent = lambda event: self.func1(event)
        self.videoWidget.mouseReleaseEvent = lambda event: self.func2(event)
        x, y = pyautogui.position()
        vid = cv2.VideoCapture(self.video_name)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.tabbar.hide()
        self.master.widget.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.master.widget.show()
        self.status_play_bar(False)
        self.master.set_dimentions(round(width / 5), round(height / 5))
        if not event:
            self.master.widget.setGeometry(
                x - int(self.videoWidget.width() / 2) - 3 * int(self.master.width / 2),
                y - int(self.videoWidget.height() / 2) - 3 * int(self.master.height / 2),
                self.master.width,
                self.master.height,
            )
        if event:
            self.master.widget.setGeometry(
                    x - int(width / 10),
                    y - int(height / 10),
                    self.master.width,
                    self.master.height,
                )
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.tab.setMouseTracking(True)
        self.tab.mouseMoveEvent = lambda event: self.moving_window(event)
        self.videoWidget.mouseDoubleClickEvent = lambda event: self.change_size(event)

    def change_size(self, event):
        self.videoWidget.mousePressEvent = lambda event: None
        self.videoWidget.mouseReleaseEvent = lambda event: None
        x, y = pyautogui.position()
        self.master.widget.setWindowFlags(
            self.master.widget.windowFlags() & ~Qt.FramelessWindowHint
        )
        self.master.widget.setWindowFlags(
            self.master.widget.windowFlags() & ~Qt.WindowStaysOnTopHint
        )
        self.master.widget.show()
        self.tabbar.show()
        self.status_play_bar(True)
        self.master.set_dimentions(*self.window.dimensions)
        self.master.widget.setGeometry(
            x - int(self.master.width / 2),
            y - int(self.master.height / 2),
            self.master.width,
            self.master.height,
        )
        self.layout.setContentsMargins(*FirstTab.marg)
        self.tab.mouseMoveEvent = lambda event: None
        self.tab.setMouseTracking(False)
        # self.videoWidget.mouseDoubleClickEvent = lambda event: None
        self.videoWidget.mouseDoubleClickEvent = lambda event : self.change_size2(event)

    @property
    def layout(self):
        return self.tab.layout()

    def creating_short_cuts(self):
        shortcut = QShortcut(QKeySequence(Qt.Key_Right), self.tab)
        shortcut.activated.connect(lambda: self.forward(5))
        shortcut = QShortcut(QKeySequence(Qt.Key_Left), self.tab)
        shortcut.activated.connect(lambda: self.backward(5))
        shortcut = QShortcut(QKeySequence(Qt.Key_Up), self.tab)
        shortcut.activated.connect(lambda: self.volumeup(5))
        shortcut = QShortcut(QKeySequence(Qt.Key_Down), self.tab)
        shortcut.activated.connect(lambda: self.volumedown(5))
        shortcut = QShortcut(QKeySequence(Qt.Key_Space), self.tab)
        shortcut.activated.connect(self.play)
        shortcut = QShortcut(QKeySequence(Qt.ControlModifier + Qt.Key_Up), self.tab)
        shortcut.activated.connect(lambda: self.volumeup(100))
        shortcut = QShortcut(QKeySequence(Qt.ControlModifier + Qt.Key_Down), self.tab)
        shortcut.activated.connect(lambda: self.volumedown(100))

    def forward(self, value):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + value * 1000)

    def backward(self, value):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - value * 1000)

    def volumeup(self, value):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + value)
        self.slider_sound.setValue(self.slider_sound.value() + value)

    def volumedown(self, value):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - value)
        self.slider_sound.setValue(self.slider_sound.value() - value)

    def status_play_bar(self, status: bool):
        self.playbutton.setVisible(status)
        self.soundbutton.setVisible(status)
        self.slider_sound.setVisible(status)
        self.slider.setVisible(status)
        self.start_time_lbl.setVisible(status)
        self.end_time_lbl.setVisible(status)
        self.size_button.button.setVisible(status)

    def creating_layout(self, *positions):
        horizontallayout = QHBoxLayout()
        horizontallayout.addWidget(self.playbutton, 1)
        horizontallayout.addWidget(self.soundbutton, 1)
        horizontallayout.addWidget(self.slider_sound, 10)
        horizontallayout.addWidget(self.start_time_lbl)
        horizontallayout.addWidget(self.slider, 70)
        horizontallayout.addWidget(self.end_time_lbl)
        horizontallayout.addWidget(self.size_button.button, 1)
        layout = QVBoxLayout()
        layout.setContentsMargins(*positions)
        layout.addWidget(self.videoWidget)
        layout.addLayout(horizontallayout)
        self.tab.setLayout(layout)

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

    def open_movie(self, name):
        self.video_name = name
        media = QMediaContent(QUrl.fromLocalFile(name))
        self.mediaPlayer.setMedia(media)

    def slider_position_change(self, position):
        self.slider.setValue(position)
        time = QTime(0, 0, 0, 0).addMSecs(self.mediaPlayer.position())
        self.start_time_lbl.setText(time.toString())

    def slider_duration_change(self, position):
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
            self.soundbutton.setIcon(
                self.tab.style().standardIcon(QStyle.SP_MediaVolume)
            )

    def exit_func(self, event=None, next_window=False):
        from open_window import OpenWindow

        if self.__dict__.get("mediaPlayer"):
            self.mediaPlayer.stop()
            del self.mediaPlayer
        if next_window:
            self.master.set_widget(OpenWindow)
            del self.master.windows["SpotifyWindow"]

    def func_for_exit(self, data):
        MyMsgBox(
            **data,
            Yeah=[QMessageBox.YesRole, lambda: self.exit_func(next_window=True)],
            Nope=[QMessageBox.NoRole, lambda: None],
        )


class SpotifyWindow:
    dimensions = (800, 800)

    def __init__(self, master):
        self.master = master
        self.window = QTabWidget()
        self.window.dimensions = self.dim
        self.tab1 = FirstTab(self.master, self.window, "tab1")
        self.tab2 = MyTab(self.master, self.window, "tab2")

        self.tab3 = MyTab(self.master, self.window, "tab3")
        self.tab4 = MyTab(self.master, self.window, "tab4")

    @property
    def dim(self):
        return SpotifyWindow.dimensions
