import subprocess
import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication


class SaveGameMangerQt(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = None
        self.btn_exit = None
        self.btn_start_game = None
        uic.loadUi('../assets/mainwindow.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self._generate_buttons()

    def _generate_buttons(self):
        #Buttons
        self.btn_start_game.clicked.connect(self.start_dsp)
        self.btn_exit.clicked.connect(self.exit)


    def start_dsp(self):
           subprocess.Popen(rf"{self.config.get('steam_path')} -applaunch 1366540")


    def exit(self):
        self.destroy()
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SaveGameMangerQt()
    sys.exit(app.exec())
