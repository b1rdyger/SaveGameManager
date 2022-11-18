import os

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget


class LogoffTimerQt(QWidget):
    timer = None

    def __init__(self, root_dir, parent=None):
        super(LogoffTimerQt, self).__init__(parent)
        self.parent = parent
        self.root_dir = root_dir
        self.ui = uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'logoff_timer.ui')
        self.__setup()

    def __setup(self):
        self.ui.btn_set_timer.clicked.connect(self.logofftimer_set)
        self.ui.btn_cancel_timer.clicked.connect(self.logofftimer_cancel)
    def show(self):
        self.ui.show()

    def close(self):
        self.ui.hide()

    def logofftimer_set(self):
        self.timer = '1234'
        print('foo')

    def logofftimer_cancel(self):
        self.timer = None
        print('bar')
