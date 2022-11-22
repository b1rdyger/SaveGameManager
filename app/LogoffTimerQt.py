import datetime
import os

from PyQt6 import uic, QtCore, QtGui
from PyQt6.QtWidgets import QWidget

from app.SGMSignals.LTSignals import LTSignals
from app.uiInterfaces.LogoffTimerUi import LogoffTimerUi
from app.utils.DateUtils import DateUtils


class LogoffTimerQt(QWidget):
    ui: LogoffTimerUi
    shutdown_after = None
    want_shutdown_after = None
    logoff_inactive = "QLabel { background-color : lime; color : black; }"
    logoff_active = "QLabel { background-color : red; color : black; }"

    def __init__(self, root_dir, parent=None):
        super().__init__()
        self.parent = parent
        self.root_dir = root_dir
        self.ui = uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'logoff-timer.ui')
        self.__setup()
        self.signals = LTSignals()
        QtCore.QDir.addSearchPath('icons', self.root_dir + os.sep + 'assets')
        logo = QtGui.QIcon('icons:logo/disk1-256.png')
        self.ui.setWindowIcon(logo)

    def __setup(self):
        self.ui.btn_set_timer.clicked.connect(self.logoff_set_timer)
        self.ui.btn_cancel_timer.clicked.connect(self.logoff_cancel_timer)
        self.ui.btn_quit_timer.clicked.connect(self.logoff_quit_timer)
        self.ui.logoff_dial.valueChanged.connect(self.dial_value_changed)
        self.dial_value_changed(0)

    def get_minutes(self, value=None):
        if value is None:
            value = self.ui.logoff_dial.value()
        return value * 10

    def dial_value_changed(self, value):
        minutes_in_future = self.get_minutes(value)
        real_minutes_in_future = max(1, self.get_minutes(value))
        self.ui.logoff_ic.display(minutes_in_future)
        self.want_shutdown_after = datetime.datetime.now()
        self.want_shutdown_after = self.want_shutdown_after + datetime.timedelta(seconds=real_minutes_in_future * 60)
        self.ui.logoff_time_status.setText(
            f'Possible logofftime: {DateUtils.get_formated_time(self.want_shutdown_after)} ')

    def show(self):
        self.ui.show()

    def close(self):
        self.ui.hide()

    def logoff_set_timer(self):
        self.shutdown_after = self.want_shutdown_after
        self.ui.logoff_time_status.setText(f'Time was set to {DateUtils.get_formated_time(self.shutdown_after)}')
        self.signals.timer_set.emit(self.shutdown_after)

    def logoff_cancel_timer(self):
        self.shutdown_after = None
        self.dial_value_changed(0)
        self.ui.logoff_dial.setValue(0)
        self.ui.logoff_time_status.setText('Reset Timer')
        self.signals.timer_clear.emit()

    def logoff_quit_timer(self):
        self.ui.hide()
