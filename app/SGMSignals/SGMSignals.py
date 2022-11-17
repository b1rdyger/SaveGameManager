import PyQt6
from PyQt6 import QtCore

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class SGMSignals(SGMSignalObjects):

    run_engine: PyQt6.QtCore.pyqtSignal = PyQt6.QtCore.pyqtSignal()
    stop_engine: PyQt6.QtCore.pyqtSignal = PyQt6.QtCore.pyqtSignal()

