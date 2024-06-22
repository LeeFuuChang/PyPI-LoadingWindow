from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

import time
import sys
import os

from .Threading import TaskThread



class AbstractLoadingWindow(QWidget):
    __application: QApplication = None

    text: str = ""
    progress: int = 0

    displayLoadingStatusSignal = pyqtSignal()

    loadingTaskIndex = -1
    loadingTasks = []

    appIconPath: str = os.path.join(os.path.dirname(__file__), "default-loading-icon.png")
    splashArtPath: str = os.path.join(os.path.dirname(__file__), "default-loading-splash.png")

    retries = 3

    width: int = 500
    height: int = 300
    barHeight: int = 30
    verticalPadding: int = 30
    horizontalPadding: int = 30
    fontSize: int = 10
    fontColor: str = "#000000"


    def __init__(self):
        self.__application = QApplication([*sys.argv, "--ignore-gpu-blacklist"])

        super(AbstractLoadingWindow, self).__init__()

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
        sys.exit(self.__application.exec_())


    def setupComponents(self):
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
        self.appIconPath = path
        self.updateStyle()


    def setSplashArtPath(self, path: str):
        self.splashArtPath = path
        self.updateStyle()


    def updateStyle(self):
        if(self.appIconPath): self.setWindowIcon(QIcon(self.appIconPath))
        if(self.splashArtPath): self.LoadingSplashArt.setPixmap(QPixmap(self.splashArtPath))

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


    def setRetries(self, retries):
        self.retries = retries


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
            tries=self.retries, 
            onFinished=self.loadNext
        ).start()


    def loadFinished(self):
        time.sleep(1)
        os._exit(0)


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




