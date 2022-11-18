import datetime
import os

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget

from app.uiInterfaces.LogoffTimerUi import LogoffTimerUi


class LogoffTimerQt(QWidget):
    ui: LogoffTimerUi
    shutdown_after = None
    want_shutdown_after = None

    def __init__(self, root_dir, parent=None):
        super(LogoffTimerQt, self).__init__(parent)
        self.parent = parent
        self.root_dir = root_dir
        self.ui = uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'logoff_timer.ui')
        self.__setup()

    def __setup(self):
        self.ui.btn_set_timer.clicked.connect(self.logoff_timer_set)
        self.ui.btn_cancel_timer.clicked.connect(self.logoff_timer_cancel)
        self.ui.logoff_dial.valueChanged.connect(self.dial_value_changed)

    def get_minutes(self, value=None):
        if value is None:
            value = self.ui.logoff_dial.value()
        return value * 10

    def dial_value_changed(self, value):
        minutes_in_future = self.get_minutes(value)
        self.ui.logoff_ic.display(minutes_in_future)
        self.want_shutdown_after = datetime.datetime.now
        self.want_shutdown_after = datetime.timedelta(seconds=minutes_in_future*60)

    def show(self):
        self.ui.show()

    def close(self):
        self.ui.hide()

    def logoff_timer_set(self):
        self.shutdown_after = self.want_shutdown_after

    def logoff_timer_cancel(self):
        self.shutdown_after = None
