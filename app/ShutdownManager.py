import contextlib
import os
from datetime import datetime

from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot, QObject

from app.SGMSignals.EngineSignals import EngineSignals
from app.SGMSignals.LTSignals import LTSignals
from app.SGMSignals.PCSignals import PCSignals


class ShutdownManager(QObject):
    want_logoff = False
    logoff_time = None

    __shutdown_after_kill = False
    __shutdown_came_from_lt = False

    def __init__(self, config):
        super().__init__()
        self.config = config

        self.signals = LTSignals()
        self.engine_signals = EngineSignals()
        self.pc_signals = PCSignals()

        self.signals.timer_set.connect(self.timer_set_emitted)
        self.signals.timer_clear.connect(self.timer_clear_emitted)

        self.engine_signals.backup_done_shutdown_allowed.connect(self.backup_done_shutdown_allowed)
        self.pc_signals.running.connect(self.shutdown)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__check_shutdown)
        self.timer.setInterval(10000)

    def set_shutdown_after_kill(self, shutdown_after_kill: bool):
        self.__shutdown_after_kill = shutdown_after_kill

    def __start_timer(self):
        self.timer.start()

    def __stop_timer(self):
        self.timer.stop()
        with contextlib.suppress(Exception):
            os.system('shutdown /a')

    def __check_shutdown(self):
        if datetime.now() >= self.logoff_time:
            self.signals.shutdown_wait_for_backup.emit()  # just console log
            self.engine_signals.want_shutdown_asap.emit()
            self.timer.stop()

    @pyqtSlot()
    def backup_done_shutdown_allowed(self):
        self.__shutdown_came_from_lt = True
        process_name = self.config['process_name']
        os.system(f"taskkill /im {process_name}")

    @pyqtSlot(bool)
    def shutdown(self, running):
        if running:
            return
        if self.__shutdown_after_kill and self.__shutdown_came_from_lt:
            self.__shutdown_came_from_lt = False  # prepared for the next try
            os.system("shutdown /s /t 60")

    @pyqtSlot(datetime)
    def timer_set_emitted(self, dt):
        self.signals.shutdown_initiated.emit(dt)
        self.logoff_time = dt
        self.__start_timer()

    @pyqtSlot()
    def timer_clear_emitted(self):
        self.signals.shutdown_abort.emit()
        self.logoff_time = None
        self.__stop_timer()
