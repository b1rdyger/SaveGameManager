import os

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLineEdit, QPlainTextEdit

class ProfileSelectorQt(QWidget):
    titleEdit: QLineEdit
    processEdit: QLineEdit
    runcommandEdit: QLineEdit
    savedirEdit: QLineEdit
    backupdirsEdit: QPlainTextEdit
    ignoredfilesEdit: QPlainTextEdit
    def __init__(self, root_dir):
        super().__init__()
        self.root_dir = root_dir
        self.ui = uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'profile-selector.ui')
        self.__setup()
        self.ui.show()
    def __setup(self):
        pass
