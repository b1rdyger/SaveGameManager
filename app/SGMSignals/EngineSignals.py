from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class EngineSignals(SGMSignalObjects):
    shutdown_allowed = pyqtSignal()