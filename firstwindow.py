import enum
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QScrollArea,
    QGroupBox,
)

import json

# import requests
from youtubesearchpython import VideosSearch
from components import MyButtonwithImage, MyLabelwithText
from PyQt5.QtCore import (
    Qt,
    QRect,
    QSize,
    pyqtSignal,
    QObject,
    QUrl,
    QPropertyAnimation,
    QPoint,
    pyqtProperty,
)
import os
from videowidget import CustomVideoPlayer
from PyQt5.QtGui import QPixmap, QIcon, QImage, QColor
from base_tab import MyTab


class Status(enum.Enum):
    START = enum.auto()
    STOP = enum.auto()


class Play_button:
    def __init__(self, image=True):
        self.status = Status.START
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.button.setIconSize(QSize(30, 30))
        self.button.setObjectName("play_stop_button")
        if image:
            self.image1 = QIcon(rf"{os.getcwd()}/images/play.png")
            self.image2 = QIcon(rf"{os.getcwd()}/images/stop.png")
            self.button.setCursor(Qt.OpenHandCursor)
            self.set_icon()
        else:
            self.image1 = QIcon(rf"{os.getcwd()}/images/empty.png")
            self.button.setIcon(self.image1)

    def set_icon(self):
        if self.status == Status.START:
            self.button.setIcon(self.image1)
        else:
            self.button.setIcon(self.image2)

    @property
    def play_status(self):
        return self.status

    @play_status.setter
    def play_status(self, value):
        if value == Status.STOP:
            self.status = Status.STOP
            self.set_icon()
        else:
            self.status = Status.START
            self.set_icon()


class MySingal(QObject):
    signal = pyqtSignal(str)


class ForLabel:
    def __init__(
        self,
        master,
        index,
        song,
        title,
        author,
        length,
        uncheck_function=None,
        maximum_height=None,
    ):
        self.signal = MySingal()
        self.tab = master
        self.song = song
        self.uncheck_function = uncheck_function
        self.titleLabel = QLabel()
        self.titleLabel.setFixedWidth(400)
        self.titleLabel.setText(title)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.authorlabel = QLabel()
        self.authorlabel.setText(author)
        self.authorlabel.setFixedWidth(190)
        self.titleLabel.setWordWrap(True)
        self.timelabel = QLabel()
        if uncheck_function:
            self.playbutton = Play_button()
            self.playbutton.button.clicked.connect(lambda: self.command(song))
            # self.playbutton.button.clicked.connect(lambda : self.signal.signal.emit(f"/home/filip/Documents/qt-learning/songs/{title}.mp4"))
        else:
            self.playbutton = Play_button(image=False)
            self.playbutton.button.clicked.connect(lambda: None)
        if isinstance(length, int):
            minutes = length // 60
            seconds = length % 60
            if minutes < 10:
                minutes = str(f"0{minutes}")
            if seconds < 10:
                seconds = str(f"0{seconds}")
            self.timelabel.setText(f"{minutes}:{seconds}")
        else:
            self.timelabel.setText(length)
        self.indexlabel = QLabel()
        self.indexlabel.setText(str(index))
        self.indexlabel.setFixedWidth(30)
        self.indexlabel.setAlignment(Qt.AlignCenter)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.indexlabel, 1)
        self.layout.addWidget(self.titleLabel, 60)
        self.layout.addWidget(self.authorlabel, 30)
        self.layout.addWidget(self.timelabel, 9)
        self.layout.addWidget(self.playbutton.button, 1)
        self.layout.setObjectName("songs_layout")
        self.authorlabel.setObjectName("songs")
        self.titleLabel.setObjectName("songs")
        self.timelabel.setObjectName("songs")
        self.indexlabel.setObjectName("songs")
        if maximum_height:
            self.indexlabel.setMaximumHeight(maximum_height)
            self.timelabel.setMaximumHeight(maximum_height)
            self.authorlabel.setMaximumHeight(maximum_height)
            self.titleLabel.setMaximumHeight(maximum_height)

    def delete(self):
        self.indexlabel.deleteLater()
        self.authorlabel.deleteLater()
        self.playbutton.button.deleteLater()
        self.titleLabel.deleteLater()
        self.indexlabel.deleteLater()
        self.timelabel.deleteLater()
        self.layout.deleteLater()

    def command(self, title: str):
        self.uncheck_function(self.playbutton)
        if self.playbutton.play_status == Status.START:
            self.signal.signal.emit(rf"{os.getcwd()}/songs/{title}")
            self.playbutton.play_status = Status.STOP
        else:
            self.playbutton.play_status = Status.START
            self.signal.signal.emit(None)


class MySignal6(QObject):
    signal = pyqtSignal(bool)


class PanelWithSongs:
    def __init__(self, master, main_layout):
        self.main_layout = main_layout
        self.tab = master
        # files = os.listdir("/home/filip/Documents/qt-learning/songs")
        # with open(rf"{os.getcwd()}/json_files/songs.json") as file:
        #     data = json.load(file)#to jzkox
        self.all_layouts = []
        self.signal = MySignal6()
        # self.layout = QVBoxLayout()
        self.layout = QVBoxLayout()
        self.groupbox = QGroupBox()
        self.groupbox.setStyleSheet("QGroupBox{padding-top:18px; margin-top:-18px}")
        self.groupbox.setLayout(self.layout)
        self.groupbox.setFlat(True)
        self.scroll = QScrollArea()
        self.scroll.verticalScrollBar().setCursor(Qt.SizeVerCursor)
        self.scroll.setWidget(self.groupbox)
        self.scroll.setWidgetResizable(True)
        self.layout.setObjectName("songs_layout")
        self.scroll.setObjectName("songs_layout")
        self.groupbox.setObjectName("songs_layout")

        layout = ForLabel(
            self.tab, "ID", None, "TITLE", "AUTHOR", "TIME", maximum_height=40
        )
        layout.layout.setContentsMargins(0, 0, 0, 10)
        self.layout.addLayout(layout.layout, 3)

    def post_init(self, user_login):
        self.user_login = user_login
        with open(rf"{os.getcwd()}/json_files/songs.json") as file:
            data = json.load(file)  # to jzkox
        with open(rf"{os.getcwd()}/json_files/file.json") as file:
            data_user = json.load(file)[user_login]
            data_user = data_user["songs"]
        for item in self.all_layouts:
            item.delete()
        self.all_layouts = []
        for song in data_user:
            layout = ForLabel(
                self.tab,
                len(self.all_layouts) + 1,
                song,
                data[song]["title"],
                data[song]["author"],
                data[song]["length"],
                self.uncheck,
            )
            self.all_layouts.append(layout)
            self.layout.addLayout(layout.layout, 4)
        self.signal.signal.emit(True)
        # for song in data:
        #     if song in data_user:
        #         layout = ForLabel(
        #             self.tab,
        #             len(self.all_layouts)+1,
        #             song,
        #             data[song]["title"],
        #             data[song]["author"],
        #             data[song]["length"],
        #             self.uncheck,
        #         )
        #         self.all_layouts.append(layout)
        #         self.layout.addLayout(layout.layout, 4)

    def show(self):
        # with open("json_files/songs.json") as file:
        #     data = json.load(file)
        # self.main_layout.addLayout(self.layout, 5)
        self.main_layout.addWidget(self.scroll, 5)
        self.scroll.show()

    def hide(self):
        self.main_layout.removeWidget(self.scroll)
        self.scroll.hide()

    def uncheck(self, playbutton):
        for lay in self:
            if lay.playbutton != playbutton:
                if lay.playbutton.status != Status.START:
                    lay.playbutton.play_status = Status.START

    def update_list(
        self,
    ):
        with open(rf"{os.getcwd()}/json_files/songs.json") as file:
            data = json.load(file)
        song = list(data.keys())[-1]
        index = len(self.all_layouts) + 1
        song = song[:-4]
        song = int(song)
        song = f"{song}.mp4"
        layout = ForLabel(
            self.tab,
            index,
            song,
            data[song]["title"],
            data[song]["author"],
            data[song]["length"],
            self.uncheck,
        )
        self.all_layouts.append(layout)
        self.layout.addLayout(layout.layout, 4)
        # tu musze dorzucic zeby zaktualizowalo
        with open(rf"{os.getcwd()}/json_files/file.json") as file:
            data = json.load(file)
            data[self.user_login]["songs"].append(song)
        with open(rf"{os.getcwd()}/json_files/file.json", "w") as file:
            json.dump(data, file)
        self.signal.signal.emit(True)

    def __iter__(self):
        yield from self.all_layouts


class FirstTab(MyTab):
    def __init__(self, master, window, title):
        super().__init__(master, window, title)
        with open(rf"{os.getcwd()}/json_files/data_spotify_window.json") as data:
            data = json.load(data)
        self.layout = QVBoxLayout()
        self.videoplayer = CustomVideoPlayer(
            master,
            window,
            self.tab,
            self.remove_all_items,
            self.see_all_items,
            self.layout,
        )
        self.cancel_button = MyButtonwithImage(
            self.tab,
            function_clicked=lambda: self.videoplayer.func_for_exit(
                data["message_box_cancel_window"]
            ),
            **data["cancel_button"],
        )
        self.songs_panel = PanelWithSongs(self.tab, self.layout)
        self.layout.addLayout(self.videoplayer.layout, 5)
        self.layout.addWidget(self.songs_panel.scroll, 5)  # jakos potem go wywalic
        self.layout.setContentsMargins(10, 30, 10, 55)
        self.tab.setLayout(self.layout)
        for lay in self.songs_panel:
            lay.signal.signal.connect(
                lambda title: self.videoplayer.open_movie(title)
            )  # tu jest problem
        self.videoplayer.signal.signal.connect(self.function)
        self.songs_panel.signal.signal.connect(self.updatesignalfunction)

    def updatesignalfunction(self, all):
        if not all:
            self.songs_panel.all_layouts[-1].signal.signal.connect(
                self.videoplayer.open_movie
            )
            return
        for panel in self.songs_panel:
            panel.signal.signal.connect(self.videoplayer.open_movie)

    def function(self, next=True, slider_position=0):
        # videoname = videoname.split("/")[-1]
        for index, song in enumerate(self.songs_panel):
            # if self.songs_panel.all_layouts[
            #                 index
            #             ].playbutton.status ==Status.STOP:
            #             self.songs_panel.all_layouts[
            #                 index + 1
            #             ].playbutton.button.click()
            #             break
            if self.songs_panel.all_layouts[index].playbutton.status == Status.STOP:
                try:
                    if next:
                        self.songs_panel.all_layouts[
                            index + 1
                        ].playbutton.button.click()
                    else:
                        if slider_position in range(0, 5000):
                            if index - 1 < 0:
                                raise IndexError
                            self.songs_panel.all_layouts[
                                index - 1
                            ].playbutton.button.click()
                        else:
                            self.videoplayer.backward(100)
                except (IndexError, NotImplementedError):
                    if (
                        self.songs_panel.all_layouts[index].playbutton.status
                        == Status.STOP
                    ):
                        self.songs_panel.all_layouts[index].playbutton.button.click()
                finally:
                    break

        # for index, song in enumerate(self.songs_panel):
        #     if song.song == videoname:

        #         try:
        #             if next:
        #                 self.songs_panel.all_layouts[
        #                     index + 1
        #                 ].playbutton.button.click()
        #             else:
        #                 if slider_position in range(0, 5000):
        #                     if index - 1 < 0:
        #                         raise IndexError
        #                     self.songs_panel.all_layouts[
        #                         index - 1
        #                     ].playbutton.button.click()
        #                 else:
        #                     self.videoplayer.backward(100)
        #         except (IndexError, NotImplementedError):
        #             if (
        #                 self.songs_panel.all_layouts[index].playbutton.status
        #                 == Status.STOP
        #             ):
        #                 self.songs_panel.all_layouts[index].playbutton.button.click()

    def remove_all_items(self):
        self.cancel_button.button.hide()
        self.tabbar.hide()
        self.songs_panel.hide()

    def see_all_items(self):
        self.cancel_button.button.show()
        self.tabbar.show()
        self.songs_panel.show()
