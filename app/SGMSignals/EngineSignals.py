from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class EngineSignals(SGMSignalObjects):
    want_shutdown_asap = pyqtSignal(bool)
    backup_done_shutdown_allowed = pyqtSignal()
    engine_started = pyqtSignal()
    check_safegame_folder = pyqtSignal(str)
    folder_found = pyqtSignal(str)
    set_observer_state = pyqtSignal(bool)
    set_ramdrive_state = pyqtSignal(bool)
    can_be_closed = pyqtSignal()