from PyQt6.QtWidgets import QWidget, QLineEdit, QListView, QPlainTextEdit

from app.uiInterfaces.QClazzes import QPushButtonClazz, QToolButtonClazz


class ProfileSelectorUi(QWidget):
    deleteButton: QPushButtonClazz
    toolButton: QToolButtonClazz
    toolButton2: QToolButtonClazz
    titleEdit: QLineEdit
    processEdit: QLineEdit
    runcommandEdit: QLineEdit
    savedirEdit: QLineEdit
    backupdirsEdit: QListView
    ignoredfilesEdit: QPlainTextEdit

