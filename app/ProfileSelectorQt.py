import os

from PyQt6 import uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QFileDialog

from app.uiInterfaces.ProfileSelectorUi import ProfileSelectorUi


class ProfileSelectorQt(QWidget):
    ui: ProfileSelectorUi

    def __init__(self, root_dir):
        super().__init__()
        self.root_dir = root_dir
        self.ui = uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'profile-selector.ui')
        self.__setup()
        self.ui.toolButton.clicked.connect(self.select_save_folder)
        self.ui.toolButton2.clicked.connect(self.add_backup_folder)
        self.ui.deleteButton.clicked.connect(self.delete_backup_folder)

    def __setup(self):
        self.model = QStandardItemModel()
        self.ui.backupdirsEdit.setModel(self.model)
        item = QStandardItem('Test')
        self.model.appendRow(item)

    def select_save_folder(self):
        savegame_folder = self.select_folder('Select Savegame Folder')
        self.ui.savedirEdit.setText(savegame_folder)
        return True

    def delete_backup_folder(self):
        current_select = self.ui.backupdirsEdit.currentIndex()
        if not current_select.data():
            return False
        self.model.removeRow(current_select.row())

    def add_backup_folder(self):
        backup_folder = self.select_folder('Add Backup Folder')
        item = QStandardItem(backup_folder)
        self.model.appendRow(item)
        return True

    # noinspection PyMethodMayBeStatic
    def select_folder(self, title="Select Folder"):
        return QFileDialog.getExistingDirectory(None, title)
