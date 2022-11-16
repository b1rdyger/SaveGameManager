import os
import subprocess
import sys

from PyQt6 import uic, QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QPixmap


class SaveGameManagerQt(QtWidgets.QMainWindow):
    arrow: QtWidgets.QLabel

    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir
        self.config = None
        self.btn_exit = None
        self.btn_start_game = None
        QtCore.QDir.addSearchPath('icons', self.root_dir + os.sep + 'assets')
        icon = QtGui.QPixmap('icons:arrow_right.png')
        uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'main-window.ui', self)  # Load the .ui file
        self.arrow.setPixmap(icon)
        self.show()  # Show the GUI
        self._generate_buttons()

        self.threadpool.start(self.engine)

    def _generate_buttons(self):
        # Buttons
        self.btn_start_game.clicked.connect(self.start_dsp)
        self.btn_exit.clicked.connect(self.exit)

    def start_dsp(self):
        subprocess.Popen(rf"{self.config.get('steam_path')} -applaunch 1366540")

    def exit(self):
        self.destroy()
        sys.exit()
