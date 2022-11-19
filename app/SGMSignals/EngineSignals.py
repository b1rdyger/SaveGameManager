from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class EngineSignals(SGMSignalObjects):
    want_shutdown = pyqtSignal(bool)
    shutdown_allowed = pyqtSignal()
    engine_started = pyqtSignal()
    check_safegame_folder = pyqtSignal(str)
    folder_found = pyqtSignal(str)
