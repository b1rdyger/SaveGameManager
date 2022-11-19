import contextlib
import os
from datetime import datetime

from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot, QObject

from app.SGMSignals.EngineSignals import EngineSignals
from app.SGMSignals.LTSignals import LTSignals


class ShutdownManager(QObject):
    want_logoff = False
    logoff_time = None

    def __init__(self):
        super().__init__()
        self.signals = LTSignals()
        self.engine_signals = EngineSignals()
        self.signals.timer_set.connect(self.timer_set_emitted)
        self.signals.timer_clear.connect(self.timer_clear_emitted)
        self.engine_signals.want_shutdown.connect(self.engine_want_logoff)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_shutdown)
        self.timer.setInterval(10000)

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()
        with contextlib.suppress(Exception):
            os.system('shutdown /a')

    def check_shutdown(self):
        if datetime.now() >= self.logoff_time:
            self.want_logoff = True
            self.engine_signals.shutdown_allowed.emit()
            self.signals.shutdown_wait_for_backup.emit()
        if self.want_logoff:
            os.system('shutdown /s /t 60')
            self.want_logoff = False

    @pyqtSlot(bool)
    def engine_want_logoff(self, var):
        self.want_logoff = var

    @pyqtSlot(datetime)
    def timer_set_emitted(self, dt):
        self.signals.shutdown_initiated.emit(dt)
        self.logoff_time = dt
        self.start_timer()

    @pyqtSlot()
    def timer_clear_emitted(self):
        self.signals.shutdown_abort.emit()
        self.logoff_time = None
        self.want_logoff = False
        self.stop_timer()
