from datetime import datetime

from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class LTSignals(SGMSignalObjects):
    timer_set = pyqtSignal(datetime)
    timer_clear = pyqtSignal()
    shutdown_initiated = pyqtSignal(datetime)
    shutdown_wait_for_backup = pyqtSignal()
    shutdown_abort = pyqtSignal()
    test_button = pyqtSignal()
