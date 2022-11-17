from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class FCHSignals(SGMSignalObjects):

    restored = pyqtSignal()
    cannot_use = pyqtSignal(str)
    start_observer = pyqtSignal(str)
    stop_observer = pyqtSignal()
