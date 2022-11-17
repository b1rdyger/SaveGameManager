import os
import subprocess

from PyQt6 import uic, QtCore, QtGui
from PyQt6.QtCore import QThread

from app.Engine import Engine
from app.SGMSignals.MFSSignals import MFSSignals
from app.SGMSignals.SGMSignals import SGMSignals
from app.SaveGameManagerUi import SaveGameManagerUi


class SaveGameManagerQt(SaveGameManagerUi):

    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir
        self.signals = SGMSignals()

        # init Engine Thread
        self.engine = Engine(self.root_dir)
        self.engine_thread = QThread()
        self.engine.moveToThread(self.engine_thread)
        self.engine_thread.start()

        self.config = None  # @todo
        QtCore.QDir.addSearchPath('icons', self.root_dir + os.sep + 'assets')
        icon = QtGui.QPixmap('icons:arrow_right.png')
        uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'main-window.ui', self)  # Load the .ui file
        self.arrow.setPixmap(icon)
        self.show()  # Show the GUI
        self._generate_buttons()

        self.mfs_signals = MFSSignals()
        self.bind_engine_emits()
        self.start_engine()

    def bind_engine_emits(self):
        self.signals.run_engine.connect(self.engine.run)
        self.signals.stop_engine.connect(self.engine.stop)
        self.mfs_signals.cleanedUp.connect(self.close)

    def start_engine(self):
        self.signals.run_engine.emit()

    def _generate_buttons(self):
        # Buttons
        self.btn_start_game.clicked.connect(self.start_dsp)
        self.btn_exit.clicked.connect(self.exit)
        self.btn_logoff_timer.clicked.connect(self.open_logoff_timer_window)

    def open_logoff_timer_window(self):
        self.msg_box.append('this is a Message,')

    def start_dsp(self):
        subprocess.Popen(rf"{self.config.get('steam_path')} -applaunch 1366540")

    def exit(self):
        self.signals.stop_engine.emit()
