from email import message
import json
import os
import time
from typing import Dict
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QGroupBox,
    QWidget,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QAbstractSpinBox,
    QProgressBar,
    QSizePolicy,
    QFileDialog,
    QInputDialog,
    QDialogButtonBox,
    QAbstractButton,
)
import urllib.request
from PIL import Image, ImageQt
from youtubesearchpython import VideosSearch
from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    QObject,
    QPoint,
    QTimer,
    QSize,
    QThread,
    QRunnable,
    pyqtSlot,
    QThreadPool,
    QDir,
)
from PyQt5.QtGui import QPixmap, QIcon, QImage, QMovie, QWheelEvent
from components import MyLabelwithImage, MyMsgBox
from PyQt5.QtTest import QTest


class MySingal(QObject):
    signal = pyqtSignal(dict)


class MySingal2(QObject):
    signal = pyqtSignal(int, str)


class MySingnal3(QObject):
    signal = pyqtSignal(int)
    signal2 = pyqtSignal(int, bool)


class SearchResult:
    def __init__(self, layout, data, leftmargin, rightmargin):
        self.layout = QVBoxLayout()
        self.signal = MySingal()
        self.layout.setContentsMargins(leftmargin, 0, rightmargin, 0)
        self.link = data["link"]
        imagetitle = data["thumbnails"][0]["url"]
        imagechannel = data["channel"]["thumbnails"][0]["url"]
        self.songlabel, self.songimage = self.creation_horizontal_box(
            data["title"], imagetitle
        )
        self.authorlabel, self.authorimage = self.creation_horizontal_box(
            data["channel"]["name"], imagechannel, 100
        )
        self.publishlabel, self.publishedtime = self.creation_double_box(
            "published time", data["publishedTime"]
        )
        self.durationlabel, self.duration = self.creation_double_box(
            "duration", data["duration"]
        )
        self.viewslabel, self.views = self.creation_double_box(
            "views", data["viewCount"]["text"]
        )
        self.download_button = QPushButton()
        self.download_button.setObjectName("songs")
        self.download_button.setText("SET")
        self.layout.addWidget(self.download_button)
        self.download_button.clicked.connect(
            lambda: self.signal.signal.emit(
                {
                    "entry_link": self.link,
                    "entry_title": self.songlabel.text(),
                    "entry_author": self.authorlabel.text(),
                    "entry_published_time": self.publishedtime.text(),
                    "entry_duration": self.duration.text(),
                    "entry_views": self.views.text(),
                }
            )
        )

        layout.addLayout(self.layout)

    def creation_horizontal_box(self, text, image_link: QPixmap, imagesize=160):
        file = open(".file.webp", "wb")
        file.write(urllib.request.urlopen(image_link).read())
        file.close()
        im = Image.open(".file.webp").convert("RGB")
        im.save(".file.png", "png")
        image = QPixmap(".file.png")
        horizontallayout = QHBoxLayout()
        titlelabel = QLabel()
        titlelabel.setAlignment(Qt.AlignCenter)
        titlelabel.setObjectName("songs2")
        titlelabel.setText(text)
        titlelabel.setMaximumHeight(80)
        titlelabel.setMinimumWidth(200)
        titlelabel.adjustSize()
        # titlelabel.setFixedHeight(30)
        titlelabel.setWordWrap(True)
        image = image.scaledToWidth(imagesize)
        titleimage = QLabel()
        titleimage.setPixmap(image)
        titleimage.setFixedSize(image.width(), image.height())
        titleimage.setObjectName("image_with_background2")
        horizontallayout.addWidget(titleimage, 30)
        horizontallayout.addWidget(titlelabel, 70)
        self.layout.addLayout(horizontallayout, 50)
        return titlelabel, titleimage

    def creation_double_box(self, name1: str, name2):
        horizontallayout = QHBoxLayout()
        titlelabel = QLabel()
        titlelabel.setObjectName("songs")
        titlelabel.setText(name1.upper())
        titlelabel.setAlignment(Qt.AlignCenter)
        titlelabel.setFixedHeight(30)
        titlelabel.setFixedWidth(130)
        titlelabel.setWordWrap(True)
        contentlabel = QLabel()
        contentlabel.setObjectName("songs2")
        contentlabel.setText(name2)
        contentlabel.setFixedHeight(30)
        horizontallayout.addWidget(titlelabel, 20)
        horizontallayout.addWidget(contentlabel, 80)
        self.layout.addLayout(horizontallayout, 50)
        return titlelabel, contentlabel

    def update_horizontal_box(self, text, image, textlabel, imagelabel, imagesize=160):
        file = open(".file.webp", "wb")
        file.write(urllib.request.urlopen(image).read())
        file.close()
        im = Image.open(".file.webp").convert("RGB")
        im.save(".file.png", "png")
        image = QPixmap(".file.png")
        textlabel.setText(text)
        image = image.scaledToWidth(imagesize)
        imagelabel.setPixmap(image)
        imagelabel.setFixedSize(image.width(), image.height())

    def update(self, data):
        imagetitle = data["thumbnails"][0]["url"]
        imagechannel = data["channel"]["thumbnails"][0]["url"]
        self.update_horizontal_box(
            data["title"], imagetitle, self.songlabel, self.songimage
        )
        self.update_horizontal_box(
            data["channel"]["name"],
            imagechannel,
            self.authorlabel,
            self.authorimage,
            imagesize=100,
        )
        self.duration.setText(data["duration"])
        self.publishedtime.setText(data["publishedTime"])
        self.views.setText(data["viewCount"]["text"])
        self.link = data["link"]

    def remove(self):
        self.download_button.deleteLater()
        self.authorimage.deleteLater()
        self.authorlabel.deleteLater()
        self.views.deleteLater()
        self.songimage.deleteLater()
        self.songlabel.deleteLater()
        self.publishedtime.deleteLater()
        self.duration.deleteLater()
        self.songlabel.deleteLater()
        self.durationlabel.deleteLater()
        self.viewslabel.deleteLater()
        self.publishlabel.deleteLater()
        self.layout.deleteLater()
    def set_status(self, status):
        self.download_button.setEnabled(status)
        

from base_tab import MyTab


class MyQLineEdit(QLineEdit):
    def __init__(self, object_name, placeholder):
        super(QLineEdit, self).__init__()
        self.setPlaceholderText(placeholder)
        self.setObjectName(object_name)

    # def keyPressEvent(self, event):
    #     print(event.text())
    #     return super(MyQLineEdit, self).keyPressEvent(event)


class EntryWithLabel:
    def __init__(
        self,
        layout,
        labeltext,
        placeholder,
        label_width,
        edit=True,
        label_name="songs",
        entry_name="songs_entry",
        second_name="songs_entryincorrect",
    ):
        self.base_layout = QHBoxLayout()
        self.label = QLabel()
        self.label.setObjectName(label_name)
        self.label.setText(labeltext)
        self.label.setFixedWidth(label_width)
        self.label.setAlignment(Qt.AlignCenter)
        self.entry = MyQLineEdit(entry_name, placeholder)
        if not edit:
            self.entry.setReadOnly(True)
        self.base_layout.addWidget(self.label)
        self.base_layout.addWidget(self.entry)
        self.name1 = entry_name
        self.name2 = second_name
        layout.addLayout(self.base_layout)

    def setText(self, text):
        self.entry.setText(text)

    def getText(self):
        return self.entry.text()

    def __bool__(self):
        return bool(self.entry.text())


class EntriesList:
    def __init__(self):
        self.scroll = QScrollArea()
        self.groupbox = QGroupBox()
        self.layout = QVBoxLayout()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.wheelEvent = lambda event: None
        self.entries = {}
        with open("json_files/data_spotify_window.json") as file:
            data = json.load(file)
        names = (
            "entry_title",
            "entry_author",
            "entry_published_time",
            "entry_duration",
            "entry_link",
            "entry_views",
        )
        for name in names:
            self.entries[name] = EntryWithLabel(self.layout, **data.get(name))
        self.groupbox.setLayout(self.layout)
        self.scroll.setWidget(self.groupbox)
        self.scroll.setWidgetResizable(True)

    def __getitem__(self, value):
        return self.entries[value]

    def __bool__(self):
        for entry in self.entries:
            if self.entries[entry].entry.text():
                continue
            return False
        return True

    def check(self, *args):
        def check_color(*args):
            for entry in args:
                if not self.entries[entry]:
                    self.entries[entry].entry.setObjectName(self.entries[entry].name2)
                    self.entries[entry].entry.style().polish(self.entries[entry].entry)

        def back_color(*args):
            for entry in args:
                if not self.entries[entry]:
                    self.entries[entry].entry.setObjectName(self.entries[entry].name1)
                    self.entries[entry].entry.style().polish(self.entries[entry].entry)

        check_color(*args)
        QTimer.singleShot(1000, lambda: back_color(*args))
    def set_status(self, status):
        for name in self.entries:
            self.entries[name].entry.setEnabled(status)

class FilterList:
    def __init__(self, number_of_items):
        self.signal = MySingnal3()
        self.number_of_items = number_of_items
        video = VideosSearch("Rude", limit=number_of_items)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll.horizontalScrollBar().wheelEvent()

        self.scroll.wheelEvent = lambda event: self.scroll.horizontalScrollBar().setValue(
            self.scroll.horizontalScrollBar().value() + event.angleDelta().y()
        )
        self.groupbox = QGroupBox()
        self.main_layout = QHBoxLayout()
        self.searchresults = []
        # self.groupbox.setStyleSheet("QGroupBox{padding-top:18px; margin-top:-18px}")
        result = video.result()["result"]
        for i in range(number_of_items):
            self.searchresults.append(SearchResult(self.main_layout, result[i], 5, 5))

        self.groupbox.setLayout(self.main_layout)
        self.scroll.setWidget(self.groupbox)
        self.scroll.setWidgetResizable(True)

    def update(self, name, number):
        video = VideosSearch(name, limit=number)
        result = video.result()["result"]
        if number != 0:
            QTimer.singleShot(1, lambda: self.signal.signal2.emit(number, True))

        def part2():
            if self.number_of_items < number:
                for i in range(number):
                    if i < self.number_of_items:
                        self.searchresults[i].update(result[i])

                    else:
                        self.searchresults.append(
                            SearchResult(self.main_layout, result[i], 5, 5)
                        )
                    self.signal.signal.emit(i + 1)
            else:
                for i in range(self.number_of_items):
                    if i < number:
                        self.searchresults[i].update(result[i])
                    else:
                        self.searchresults[i].remove()
                    if number != 0:
                        self.signal.signal.emit(i + 1)
                self.searchresults = self.searchresults[:number]
            self.signal.signal2.emit(number, False)
            self.number_of_items = number

        QTimer.singleShot(500, part2)
        self.scroll.horizontalScrollBar().setValue(0)
    def set_status(self, status):
        for searchresult in self.searchresults:
            searchresult.set_status(status)


class EntryWithLabelSearchedBoxAndSpinBox(EntryWithLabel):
    def __init__(
        self,
        layout,
        margin_left,
        margin_right,
        margin_up,
        labeltext,
        placeholder,
        label_width,
        spacing,
        edit=True,
        label_name="songs",
        entry_name="songs_entry",
    ):
        self.signal = MySingal2()
        super().__init__(
            layout, labeltext, placeholder, label_width, edit, label_name, entry_name
        )
        self.prograssbar = QProgressBar()
        self.prograssbar.setFixedWidth(80)
        self.base_layout.setContentsMargins(margin_left, margin_up, margin_right, 0)
        self.base_layout.setSpacing(spacing)
        self.create_spin_box()
        self.create_button()
        self.entry.returnPressed.connect(self.button.click)
        self.entry.keyPressEvent = self.keyPress
        self.base_layout.addWidget(self.spinbox)
        self.base_layout.addWidget(self.button)
        right = (
            self.base_layout.contentsMargins().right()
            - self.prograssbar.width()
            - self.base_layout.spacing()
        )

        margins = self.base_layout.contentsMargins()
        margins.setRight(right)
        self.base_layout.setContentsMargins(margins)
        self.base_layout.addWidget(self.prograssbar)
        policy = self.prograssbar.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.prograssbar.setSizePolicy(policy)
        self.prograssbar.setVisible(False)
    def set_status(self, status = False):
        self.entry.setEnabled(status)
        self.spinbox.setEnabled(status)
        self.button.setEnabled(status)


    def keyPress(self, event):
        if event.key() == Qt.Key_Up:
            self.spinbox.setValue(self.spinbox.value() + 1)
        elif event.key() == Qt.Key_Down:
            self.spinbox.setValue(self.spinbox.value() - 1)
        # self.entry.focusNextPrevChild(True) #useful
        return super(MyQLineEdit, self.entry).keyPressEvent(event)

    def get_number(self):
        return self.spinbox.text()

    def create_spin_box(self):
        self.spinbox = QSpinBox()
        self.spinbox.wheelEvent = lambda event: None
        self.spinbox.setMaximum(0)
        self.spinbox.setMaximum(15)
        self.spinbox.setValue(4)
        self.spinbox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinbox.setAlignment(Qt.AlignCenter)
        self.spinbox.setWrapping(False)

    def create_button(self):
        self.button = QPushButton()
        self.button.setText("ENTER")
        self.button.setObjectName("songs")
        self.button.setStyleSheet("padding-left:10px; padding-right:10px")
        self.button.clicked.connect(
            lambda: self.signal.signal.emit(int(self.spinbox.text()), self.entry.text())
        )

    def clicked(self):
        self.button.click()

    def func(self, movie):
        self.base_layout.addWidget(movie)


class MySignal4(QObject):
    signal = pyqtSignal(str)


from pytube import YouTube


class DownloadPanel:
    def __init__(
        self,
        layout,
        margin_left,
        margin_right,
        margin_up,
        tofile,
        normal,
        lyrics,
        spacing,
        object_name,
    ):
        self.layout = QHBoxLayout()
        self.normal_download_button = QPushButton()
        self.tofile_download_button = QPushButton()
        self.lyrics_button = QPushButton()
        self.normal_download_button.setText(normal)
        self.tofile_download_button.setText(tofile)
        self.lyrics_button.setText(lyrics)
        self.layout.setContentsMargins(margin_left, margin_up, margin_right, 0)
        self.layout.setSpacing(spacing)
        for item in (
            self.normal_download_button,
            self.tofile_download_button,
            self.lyrics_button,
        ):
            self.layout.addWidget(item)
            item.setObjectName(object_name)
        layout.addLayout(self.layout)
    def set_status(self, status):
        self.normal_download_button.setEnabled(status)
        self.lyrics_button.setEnabled(status)
        self.tofile_download_button.setEnabled(status)


class Worker(QThread):
    progress = pyqtSignal()

    def __init__(self, entries):
        self.entries_list = entries
        super().__init__()

    def run(self):
        with open(rf"{os.getcwd()}/json_files/songs.json") as data:
            data = json.load(data)
        index = list(data.keys())[-1]
        index = index[:-4]
        index = int(index)
        index += 1
        link = self.entries_list["entry_link"].getText()
        print(link)
        yt = YouTube(link)
        ys = yt.streams.filter(progressive=True).last()
        data[f"{index}.mp4"] = {
            "title": self.entries_list["entry_title"].getText(),
            "author": self.entries_list["entry_author"].getText(),
            "length": yt.length,
            "views": yt.views,
        }
        with open(rf"{os.getcwd()}/json_files/songs.json", "w") as file:
            json.dump(data, file)
        print("cosss")
        ys.download(rf"{os.getcwd()}/songs", filename=str(index) + ".mp4")


class Worker2(QThread):
    progress = pyqtSignal()
    task = pyqtSignal()

    def __init__(self, entries, path, directory_name, file_name):
        self.entries_list = entries
        self.path = path
        self.directory_name = directory_name
        self.file_name = file_name
        super().__init__()

    def run(self):
        # names = (
        #     "entry_title",
        #     "entry_author",
        #     "entry_published_time",
        #     "entry_duration",
        #     "entry_link",
        #     "entry_views",
        # )
        # ys, index = self.download()
        # filename, _ = QFileDialog.getOpenFileName(
        #     self.tab, "Open Movie", QDir.homePath() + "/filip/Documents/qt-learning"
        # )
        # if filename != "":
        # with open(rf"{os.getcwd()}/json_files/songs.json") as data:
        #     data = json.load(data)
        # index = list(data.keys())[-1]
        # index = index[:-4]
        # index = int(index)
        # index += 1
        # link = self.entries_list["entry_link"].getText()
        # name = self.entries_list["entry_title"].getText()
        # print(link)
        # yt = YouTube(link)
        # ys = yt.streams.filter(progressive=True).last()
        # data[f"{index}.mp4"] = {
        #     "title": self.entries_list["entry_title"].getText(),
        #     "author": self.entries_list["entry_author"].getText(),
        #     "length": yt.length,
        #     "views": yt.views,
        # }
        # with open(rf"{os.getcwd()}/json_files/songs.json", "w") as file:
        #     json.dump(data, file)
        # print("cosss")
        # ys.download(self.path, filename=name + ".mp4")
        if self.directory_name:
            self.path += f"/{self.directory_name}"
            os.mkdir(self.path)
        link = self.entries_list["entry_link"].getText()
        # name = self.entries_list["entry_title"].getText()
        print(link)
        yt = YouTube(link)
        ys = yt.streams.filter(progressive=True).last()
        # data[f"{index}.mp4"] = {
        #     "title": self.entries_list["entry_title"].getText(),
        #     "author": self.entries_list["entry_author"].getText(),
        #     "length": yt.length,
        #     "views": yt.views,
        # }
        # with open(rf"{os.getcwd()}/json_files/songs.json", "w") as file:
        #     json.dump(data, file)
        # print("cosss")
        ys.download(self.path, filename=self.file_name + ".mp4")


class MyInputMsg(QInputDialog):
    def __init__(self, master, window_title, window_name, args):
        self.result = list()
        self.dialog = QInputDialog(master)
        self.dialog.setObjectName(window_name)
        self.dialog.setWindowTitle(window_title)
        self.dialog.show()
        self.entries = {}
        self.dialog.findChild(QLineEdit).hide()
        self.dialog.findChild(QLabel).hide()
        self.results = {}
        for index, item in enumerate(args):
            title, entry = self.create_box(
                index,
                item["entry_width"],
                item["label_width"],
                item["entry_height"],
                item["label_height"],
                item["entry_placeholder"],
                item["label_text"],
                item["entry_name"],
            )
            self.entries[title] = entry

        self.dialog.setOkButtonText("SET")
        self.dialog.setCancelButtonText("CANCEL")
        QAbstractButton.clicked
        for index, button in enumerate(
            self.dialog.findChild(QDialogButtonBox).buttons()
        ):
            button.setIcon(QIcon())
            # button.clicked.connect(lambda : func)
            button.setFixedWidth(80)
            if index == 0:

                button.clicked.connect(lambda: self.button_command())
            print(button)
        self.dialog.exec()

    def button_command(self):
        self.results = {
            text: entry.text()
            for text, entry in zip(self.entries.keys(), self.entries.values())
        }

    def create_box(
        self,
        index,
        entrywidth,
        labelwidth,
        entry_height,
        label_height,
        placeholder,
        labeltext,
        entryname,
    ):
        layout = QHBoxLayout()
        label = QLabel()
        label.setFixedWidth(labelwidth)
        label.setText(labeltext)
        entry = QLineEdit()
        entry.focusNextPrevChild(True)
        entry.setObjectName(entryname)
        entry.setFixedWidth(entrywidth)
        entry.setPlaceholderText(placeholder)
        label.setFixedHeight(label_height)
        entry.setFixedHeight(entry_height)
        layout.addWidget(label)
        layout.addWidget(entry)
        self.dialog.layout().insertLayout(0, layout)
        if index == 0:
            layout.setContentsMargins(0, 0, 0, 15)
        return label.text(), entry


class SecondTab(MyTab):
    def __init__(self, master, window, title, number_of_items):
        super().__init__(master, window, title)
        self.filterlist = FilterList(number_of_items)
        self.entries_list = EntriesList()

        for searchbox in self.filterlist.searchresults:
            searchbox.signal.signal.connect(lambda arg: self.command_for_setter(arg))
        self.layout = QVBoxLayout(self.tab)
        self.creation_label()
        self.layout.addWidget(self.label.label, 9)
        self.layout.addWidget(self.filterlist.scroll, 9)
        self.filterlist.scroll.setVisible(False)
        self.layout.addWidget(self.entries_list.scroll, 6)
        self.layout.setContentsMargins(10, 10, 10, 15)
        with open("json_files/data_spotify_window.json") as file:
            data = json.load(file)
        self.new_song_entry = EntryWithLabelSearchedBoxAndSpinBox(
            self.layout, **data["searched_box"]
        )
        self.download_panel = DownloadPanel(self.layout, **data["download_box"])
        self.download_panel.normal_download_button.clicked.connect(
            lambda: self.download_normal_command()
            if (
                self.entries_list["entry_link"]
                and self.entries_list["entry_title"]
                and self.entries_list["entry_author"]
            )
            else self.entries_list.check("entry_link", "entry_title", "entry_author")
        )
        print(self.entries_list["entry_link"])
        self.download_panel.tofile_download_button.clicked.connect(
            lambda: self.download_to_file()
            if self.entries_list["entry_link"]
            else self.entries_list.check("entry_link")
        )
        self.filterlist.signal.signal.connect(
            lambda value: self.progressbar_command(value)
        )
        self.filterlist.signal.signal2.connect(
            lambda value, status: self.progressbar_setting_max_value(value, status)
        )
        self.new_song_entry.signal.signal.connect(
            lambda value, song_name: self.update_command(value, song_name)
        )

    def creation_label(self):
        with open(rf"{os.getcwd()}/json_files/data_spotify_window.json") as data:
            data = json.load(data)
        self.label = MyLabelwithImage(self.tab, **data["label"])
        self.label.label.setContentsMargins(20, 0, 20, 20)

    def set_spotify(self, value: bool):
        if value:
            self.filterlist.scroll.setVisible(False)
            self.label.label.setVisible(True)
        else:
            self.filterlist.scroll.setVisible(True)
            self.label.label.setVisible(False)

    def progressbar_setting_max_value(self, value, status):
        self.set_spotify(True)
        self.new_song_entry.prograssbar.setMaximum(value)
        if status:
            self.new_song_entry.prograssbar.setVisible(status)
            return
        self.new_song_entry.prograssbar.setValue(100)

        def last_part():
            if value != 0:
                if not self.filterlist.scroll.isVisible():
                    self.set_spotify(False)
            else:
                if not self.label.label.isVisible():
                    self.set_spotify(True)

        QTimer.singleShot(
            500, lambda: self.new_song_entry.prograssbar.setVisible(status)
        )
        QTimer.singleShot(500, last_part)
        QTimer.singleShot(1000, lambda: self.new_song_entry.prograssbar.setValue(0))

    def progressbar_command(self, value):
        self.new_song_entry.prograssbar.setValue(value)

    def command_for_setter(self, kwargs):
        difference = False
        if self.entries_list:
            for entry in kwargs:
                if self.entries_list[entry].getText() != kwargs[entry]:
                    difference = True
                    break

        def setting():
            for entry in kwargs:
                self.entries_list[entry].setText(kwargs[entry])

        if difference:
            with open("json_files/data_spotify_window.json") as file:
                data = json.load(file)
                data = data["new_data_button"]
            MyMsgBox(
                **data,
                Yeah=[QMessageBox.YesRole, setting],
                Nope=[QMessageBox.NoRole, lambda: None],
            )
            return
        setting()

    def command(self):
        video = VideosSearch(self.entry.text(), limit=len(self.searchresults))
        for i, x in enumerate(self.searchresults):
            x.update(video.result()["result"][i])

    def update_command(self, value, song_name):
        self.filterlist.update(song_name, value)
        for searchbox in self.filterlist.searchresults:
            searchbox.signal.signal.connect(lambda arg: self.command_for_setter(arg))

    def download_normal_command(self):
        # self.set_status(False)
        def adding_new_song():
            self.worker = Worker(self.entries_list)
            self.worker.start()
            self.worker.progress.connect(self.worker.run)
        with open("json_files/data_spotify_window.json") as file:
            data = json.load(file)
        MyMsgBox(
            **data["msgbox_add_song_local"],
            Yeah=[QMessageBox.YesRole, adding_new_song],
            Nope=[QMessageBox.NoRole, lambda : None],
        )
        # self.set_status()

    def download_to_file(self):
        self.set_status(False)
        with open("json_files/data_spotify_window.json") as file:
            data = json.load(file)
        namefile = self.entries_list["entry_title"].getText()
        while " " in namefile:
            namefile = namefile.replace(" ", "_")
        namedirectory = namefile + "_dir"
        directory = ""

        def directory_setter():
            nonlocal directory
            directory = QFileDialog.getExistingDirectory(
                self.tab, "Set directory", QDir.homePath()
            )

        def withdirectory():
            nonlocal namefile
            nonlocal namedirectory
            nonlocal directory
            directory_setter()
            if directory:
                message = MyInputMsg(self.tab, **data["msgboxinputdouble"])
                if message.results:
                    if message.results["File name:"]:
                        namefile = message.results["File name:"]
                        while " " in namefile:
                            namefile = namefile.replace(" ", "_")
                    if message.results["Directory name:"]:
                        namedirectory = message.results["Directory name:"]
                        while " " in namedirectory:
                            namedirectory = namedirectory.replace(" ", "_")
                    creation(own_directory=True)

        def withoutdirectory():
            nonlocal namefile
            nonlocal directory
            directory_setter()
            if directory:
                message = MyInputMsg(self.tab, **data["msgboxinputonce"])
                if message.results:
                    if message.results["File name:"]:
                        namefile = message.results["File name:"]
                        while " " in namefile:
                            namefile = namefile.replace(" ", "_")
                    creation()

        def creation(own_directory=False):
            if own_directory:
                self.worker = Worker2(
                    self.entries_list, directory, namedirectory, namefile
                )
            else:
                self.worker = Worker2(
                    self.entries_list,
                    directory,
                    directory_name=None,
                    file_name=namefile,
                )
            self.worker.start()
            self.worker.progress.connect(self.worker.run)

        MyMsgBox(
            **data["msgbox_directory"],
            Yeah=[QMessageBox.YesRole, withdirectory],
            Nope=[QMessageBox.NoRole, withoutdirectory],
            Cancel=[QMessageBox.RejectRole, lambda: None],
        )
        self.set_status(True)

        # file = QFileDialog.getExistingDirectory(
        #     self.tab, "Set directory", QDir.homePath()
        #     )
        #     name: str = self.entries_list["entry_title"].getText()
        #     while " " in name:
        #         name = name.replace(" ", "_")
        # MyMsgBox(
        #     **data,
        #     Yeah=[QMessageBox.YesRole, directory],
        #     Nope=[QMessageBox.NoRole, alone],
        # )
        # file = QFileDialog.getExistingDirectory(
        #     self.tab, "Set directory", QDir.homePath()
        # )
        # name: str = self.entries_list["entry_title"].getText()
        # while " " in name:
        #     name = name.replace(" ", "_")
        # os.mkdir(file + f"/{name}")
    def set_status(self, status = True):
        self.new_song_entry.set_status(status)
        self.download_panel.set_status(status)
        self.filterlist.set_status(status)
        self.entries_list.set_status(status)
        # self.download_panel.tofile_download_button.setEnabled(False)
        # self.download_panel.normal_download_button.setEnabled(False)
        # self.download_panel.lyrics_button.setEnabled(False)
