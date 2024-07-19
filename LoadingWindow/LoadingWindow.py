from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import time
import sys
import os

from .Threading import TaskThread



class LoadingWindow(QWidget):
    __application: QApplication = None

    text: str = ""
    progress: int = 0

    displayLoadingStatusSignal = pyqtSignal()

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
    barHeight: int = 30
    verticalPadding: int = 30
    horizontalPadding: int = 30
    fontSize: int = 10
    fontColor: str = "#000000"


    def __init__(self):
        self.__application = QApplication([*sys.argv, "--ignore-gpu-blacklist"])

        super(self.__class__, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("LoadingWindow")

        self.setupComponents()

        self.updateStyle()

        self.displayLoadingStatusSignal.connect(self.displayLoadingStatus)

        self.loadingTimer = QTimer(self)
        self.loadingTimer.timeout.connect(self.displayLoadingStatusSignal.emit)
        self.loadingTimer.start()
        self.setFrameRate(30)


    def exec_(self):
        self.show()
        self.loadNext()
        self.__application.exec_()
        del self.__application


    def setupComponents(self):
        self.appIcon = QIcon(self.defaultAppIconPath)
        self.splashArt = QPixmap(self.defaultSplashArtPath)

        self.LoadingSplashArt = QLabel(self)
        self.LoadingSplashArt.setScaledContents(True)
        self.LoadingSplashArt.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.LoadingProgress = QProgressBar(self)
        self.LoadingProgress.setRange(0, 100)
        self.LoadingProgress.setTextVisible(False)
        self.LoadingProgress.setOrientation(Qt.Horizontal)

        self.LoadingStatus = QLabel(self)
        self.LoadingStatus.setText(self.text)
        self.LoadingStatus.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.ProgressLabel = QLabel(self)
        self.ProgressLabel.setText(f"{self.progress}%")
        self.ProgressLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


    def setSize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.updateStyle()


    def setBarHeight(self, barHeight: int):
        self.barHeight = barHeight
        self.updateStyle()


    def setFontSize(self, fontSize: int):
        self.fontSize = fontSize
        self.updateStyle()


    def setPadding(self, v: int, h: int):
        self.verticalPadding = v
        self.horizontalPadding = h
        self.updateStyle()


    def setIconPath(self, path: str):
        self.appIcon = QIcon(path)
        self.updateStyle()


    def setIconURL(self, url: str):
        data = urllib.request.urlopen(url).read()
        pmap = QPixmap()
        pmap.loadFromData(data)
        self.appIcon = QIcon(pmap)
        self.updateStyle()


    def setSplashArtPath(self, path: str):
        self.splashArt = QPixmap(path)
        self.updateStyle()


    def setSplashArtURL(self, url: str):
        data = urllib.request.urlopen(url).read()
        self.splashArt = QPixmap()
        self.splashArt.loadFromData(data)
        self.updateStyle()


    def updateStyle(self):
        if(self.appIcon): self.setWindowIcon(self.appIcon)
        if(self.splashArt): self.LoadingSplashArt.setPixmap(QPixmap(self.splashArt))

        geometry = [
            self.horizontalPadding,
            self.height - self.verticalPadding - self.barHeight,
            self.width - self.horizontalPadding*2,
            self.barHeight
        ]

        self.LoadingSplashArt.setGeometry(0, 0, self.width, self.height)
        self.LoadingProgress.setGeometry(*geometry)
        self.LoadingStatus.setGeometry(*geometry)
        self.ProgressLabel.setGeometry(*geometry)

        self.LoadingStatus.font().setPointSize(self.fontSize)
        self.ProgressLabel.font().setPointSize(self.fontSize)

        self.LoadingStatus.setStyleSheet(f"color: {self.fontSize}; padding:0 {int(self.horizontalPadding/2)}px;")
        self.ProgressLabel.setStyleSheet(f"color: {self.fontSize}; padding:0 {int(self.horizontalPadding/2)}px;")


    def setFrameRate(self, frameRate):
        self.loadingTimer.setInterval(round(1000/frameRate))


    def setTasks(self, tasks):
        if(self.loadingTaskIndex != -1):
            raise AssertionError("Cannot set tasks after loading process started!")
        self.loadingTasks = tasks


    def setTaskRetries(self, retries):
        self.taskRetries = retries


    def setPreserveTime(self, t):
        self.preserveTime = max(0, t)


    def displayLoadingStatus(self):
        self.LoadingStatus.setText(self.text)
        self.LoadingStatus.repaint()
        self.ProgressLabel.setText(f"{self.progress}%")
        self.ProgressLabel.repaint()
        self.LoadingProgress.setValue(self.progress)
        self.LoadingProgress.repaint()


    def loadNext(self):
        self.loadingTaskIndex += 1
        self.displayLoadingStatusSignal.emit()
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




