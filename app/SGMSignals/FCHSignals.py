from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class FCHSignals(SGMSignalObjects):

    renamed = pyqtSignal(str)
    start_rename = pyqtSignal()
    restored = pyqtSignal(str)
    not_restored = pyqtSignal(str)
    cannot_use = pyqtSignal(str)
    start_observer = pyqtSignal(str)
    stop_observer = pyqtSignal()
    backup_successful = pyqtSignal()
