import PyQt6
from PyQt6 import QtCore
from PyQt6.QtCore import QObject


class SGMSignals(QObject):

    run_engine: PyQt6.QtCore.pyqtSignal = PyQt6.QtCore.pyqtSignal()
    stop_engine: PyQt6.QtCore.pyqtSignal = PyQt6.QtCore.pyqtSignal()

