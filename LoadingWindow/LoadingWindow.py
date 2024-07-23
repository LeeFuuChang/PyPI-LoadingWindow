from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QLabel, QFrame
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from typing import Tuple, List, Callable

import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import time
import sys
import os

from .Threading import TaskThread





class ProgressBar(QFrame):
    text: str = ""
    progress: int = 0

    padding: Tuple[int, int] = (0, 16)

    fontSize: int = 10
    fontColor: str = "#000000"

    filledColor: str = "#69ca67"
    backgroundColor: str = "#ffffff"


    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)

        self.setupComponents()

        self.updateStyle()


    def setText(self, text: str):
        """
        Set the Loading Status Text
        ```
        ProgressBar.setText("Loading . . .") # this will auto re-render
        # or
        LoadingWindow.progressBar.text = "Loading . . ."
        LoadingWindow.progressBar.updateStyle() # re-render
        ```
        """
        self.text = text
        self.updateStyle()


    def setProgress(self, progress: int):
        """
        Set the Loading Progress Value
        ```
        ProgressBar.setProgress(0) # 0 ~ 100 # this will auto re-render
        # or
        LoadingWindow.progressBar.progress = 0 # 0 ~ 100
        LoadingWindow.progressBar.updateStyle() # re-render
        ```
        """
        self.progress = progress
        self.updateStyle()


    def setPadding(self, v: int, h: int):
        """
        Set the Padding of ProgressBar Text
        > this changes including status text and progress text
        ```
        ProgressBar.setPadding(0, 16) # Vertical and Horizontal # this will auto re-render
        # or
        LoadingWindow.progressBar.padding = (0, 16) # Vertical and Horizontal
        LoadingWindow.progressBar.updateStyle() # re-render
        ```
        """
        self.padding = (v, h)
        self.updateStyle()


    def setFontSize(self, fontSize: int):
        """
        Set the ProgressBar Text's FontSize:
        ```python
        ProgressBar.setFontSize(10) # this will auto re-render
        # or
        LoadingWindow.setFontSize(10) # this will auto re-render
        # or
        LoadingWindow.progressBar.fontSize = 10
        LoadingWindow.progressBar.updateStyle() # re-render
        ```
        """
        self.fontSize = fontSize
        self.updateStyle()


    def setFontColor(self, fontColor: str):
        """
        Set the ProgressBar Text's FontColor:
        ```python
        ProgressBar.setFontColor("#000000") # this will auto re-render
        # or
        LoadingWindow.setFontColor("#000000") # this will auto re-render
        # or
        LoadingWindow.progressBar.fontColor = "#000000"
        LoadingWindow.progressBar.updateStyle() # re-render
        ```
        """
        self.fontColor = fontColor
        self.updateStyle()


    def setFilledColor(self, filledColor: str):
        """
        Set the ProgressBar filled area's Color
        ```python
        ProgressBar.setFilledColor("#69ca67")
        ```
        """
        self.filledColor = filledColor
        self.updateStyle()


    def setBackgroundColor(self, backgroundColor: str):
        """
        Set the ProgressBar track's Color
        ```python
        ProgressBar.setBackgroundColor("#ffffff")
        ```
        """
        self.backgroundColor = backgroundColor
        self.updateStyle()


    def setupComponents(self):
        self.filledArea = QFrame(self)

        self.statusLabel = QLabel(self)
        self.statusLabel.setText(self.text)
        self.statusLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.progressLabel = QLabel(self)
        self.progressLabel.setText(f"{self.progress}%")
        self.progressLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


    def updateStyle(self):
        self.setStyleSheet(f"background-color: {self.backgroundColor}")

        self.filledArea.setGeometry(0, 0, round(self.width()*self.progress/100), self.height())
        self.filledArea.setStyleSheet(f"background-color: {self.filledColor}")

        self.statusLabel.setText(self.text)
        self.statusLabel.font().setPointSize(self.fontSize)
        self.statusLabel.setGeometry(0, 0, self.width(), self.height())
        self.statusLabel.setStyleSheet(f"color: {self.fontColor}; padding: {self.padding[0]}px {self.padding[1]}px; background-color: transparent")

        self.progressLabel.setText(f"{self.progress}%")
        self.progressLabel.font().setPointSize(self.fontSize)
        self.progressLabel.setGeometry(0, 0, self.width(), self.height())
        self.progressLabel.setStyleSheet(f"color: {self.fontColor}; padding: {self.padding[0]}px {self.padding[1]}px; background-color: transparent")

        self.repaint()





class LoadingWindow(QWidget):
    __application: QApplication = None

    text: str = ""
    progress: int = 0

    updateStatusSignal = pyqtSignal()

    loadingTaskIndex = -1
    loadingTasks = []

    appIcon: QIcon = None
    defaultAppIconPath: str = os.path.join(os.path.dirname(__file__), "default-loading-icon.png")

    splashArt: QPixmap = None
    defaultSplashArtPath: str = os.path.join(os.path.dirname(__file__), "default-loading-splash.png")

    taskRetries: int = 3
    preserveTime: int = 1

    width: int = 500
    height: int = 300
    padding: Tuple[int, int] = (32, 32)
    barHeight: int = 24


    def __init__(self):
        self.__application = QApplication([*sys.argv, "--ignore-gpu-blacklist"])

        super(self.__class__, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("LoadingWindow")

        self.setupComponents()

        self.updateStyle()

        self.updateStatusSignal.connect(self.updateStatus)

        self.loadingTimer = QTimer(self)
        self.loadingTimer.timeout.connect(self.updateStatusSignal.emit)
        self.loadingTimer.start()
        self.setFrameRate(30)


    def setSize(self, width: int, height: int):
        """
        Set the Size of the loading Window:
        ```python
        LoadingWindow.setSize(500, 300) # Width and Height
        ```
        """
        self.width = width
        self.height = height
        self.updateStyle()


    def setPadding(self, v: int, h: int):
        """
        Set distance between the Window's Edge and the ProgressBar:
        ```python
        LoadingWindow.setPadding(30, 30) # Vertical and Horizontal
        ```
        """
        self.padding = (v, h)
        self.updateStyle()


    def setBarHeight(self, barHeight: int):
        """
        Set the Height of the ProgressBar:
        ```python
        LoadingWindow.setBarHeight(24)
        ```
        """
        self.barHeight = barHeight
        self.updateStyle()


    def setFontSize(self, fontSize: int):
        """
        Set the Loading Status Text's FontSize:
        ```python
        LoadingWindow.setFontSize(10)
        ```
        """
        self.progressBar.fontSize = fontSize
        self.updateStyle()


    def setFontColor(self, fontColor: str):
        """
        Set the Loading Status Text's FontColor:
        ```python
        LoadingWindow.setFontColor("#000000")
        ```
        """
        self.progressBar.fontColor = fontColor
        self.updateStyle()


    def setIconPath(self, path: str):
        """
        Set Loading Window's Icon (By file path):
        >> this only works after packing into an executable
        ```python
        LoadingWindow.setIconPath("./Path/To/Your/Icon")
        ```
        """
        self.appIcon = QIcon(path)
        self.updateStyle()


    def setIconURL(self, url: str):
        """
        Set Loading Window's Icon (By image url):
        > this only works after packing into an executable
        ```python
        LoadingWindow.setIconURL("./URL/To/Your/Icon")
        ```
        """
        data = urllib.request.urlopen(url).read()
        pmap = QPixmap()
        pmap.loadFromData(data)
        self.appIcon = QIcon(pmap)
        self.updateStyle()


    def setSplashArtPath(self, path: str):
        """
        Set Loading Splash Image (By file path):
        ```python
        LoadingWindow.setSplashArtPath("./Path/To/Your/Image")
        ```
        """
        self.splashArt = QPixmap(path)
        self.updateStyle()


    def setSplashArtURL(self, url: str):
        """
        Set Loading Splash Image (By image url):
        ```python
        LoadingWindow.setSplashArtURL("./URL/To/Your/Image")
        ```
        """
        data = urllib.request.urlopen(url).read()
        self.splashArt = QPixmap()
        self.splashArt.loadFromData(data)
        self.updateStyle()


    def setFrameRate(self, frameRate: int):
        """
        Set Loading Window FrameRate:
        ```python
        LoadingWindow.setFrameRate(30)
        ```
        """
        self.loadingTimer.setInterval(round(1000/frameRate))


    def setPreserveTime(self, t: int):
        """
        Set How long (in seconds) the loading windows stays after all tasks completed:
        ```python
        LoadingWindow.setPreserveTime(1)
        ```
        """
        self.preserveTime = max(0, t)


    def setTasks(self, tasks: List[Callable]):
        """
        Set Tasks to load:
        ```python
        LoadingWindow.setTasks([func1, func2, ...])
        ```
        """
        if(self.loadingTaskIndex != -1):
            raise AssertionError("Cannot set tasks after loading process started!")
        self.loadingTasks = tasks


    def setTaskRetries(self, retries: int):
        """
        Set Tasks retries:
        ```python
        LoadingWindow.setTaskRetries(3)
        ```
        """
        if(self.loadingTaskIndex != -1):
            raise AssertionError("Cannot set task retries after loading process started!")
        self.taskRetries = retries


    def setupComponents(self):
        self.appIcon = QIcon(self.defaultAppIconPath)
        self.splashArt = QPixmap(self.defaultSplashArtPath)

        self.splashArtLabel = QLabel(self)
        self.splashArtLabel.setScaledContents(True)
        self.splashArtLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.progressBar = ProgressBar(self)


    def updateStyle(self):
        if(self.appIcon): self.setWindowIcon(self.appIcon)
        if(self.splashArt): self.splashArtLabel.setPixmap(QPixmap(self.splashArt))

        self.splashArtLabel.setGeometry(0, 0, self.width, self.height)

        self.progressBar.setGeometry(
            self.padding[1],
            self.height - self.padding[0] - self.barHeight,
            self.width - self.padding[1]*2,
            self.barHeight,
        )
        self.progressBar.updateStyle()


    def updateStatus(self):
        self.progressBar.text = self.text
        self.progressBar.progress = self.progress
        self.progressBar.updateStyle()


    def loadNext(self):
        self.loadingTaskIndex += 1
        self.updateStatusSignal.emit()
        if(self.loadingTaskIndex >= len(self.loadingTasks)): return self.loadFinished()
        self.loadingThreadWorker = TaskThread(
            target=self.loadingTasks[self.loadingTaskIndex], 
            delay=0.1,
            tries=self.taskRetries, 
            onFinished=self.loadNext
        ).start()


    def loadFinished(self):
        time.sleep(self.preserveTime)
        self.deleteLater()
        self.__application.quit()


    def closeEvent(self, e):
        self.loadingTimer.stop()
        super().closeEvent(e)
        os._exit(0)


    def showEvent(self, e):
        super().showEvent(e)
        self.move(
            int((QApplication.primaryScreen().size().width() - self.width) / 2), 
            int((QApplication.primaryScreen().size().height() - self.height) / 2)
        )


    def exec_(self):
        self.show()
        self.loadNext()
        self.__application.exec_()
        del self.__application





