from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class Worker(SGMSignalObjects):
    progress = pyqtSignal()