from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class PCSignals(SGMSignalObjects):

    running = pyqtSignal(bool)
