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
    folder_not_found = pyqtSignal(str)
    folder_created = pyqtSignal(str)
    broken_link = pyqtSignal(str)
    backup_start = pyqtSignal()
    backup_fails = pyqtSignal()
    backuped_up_file = pyqtSignal(str)
    smart_backup_finished = pyqtSignal()



