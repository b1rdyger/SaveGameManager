from PyQt6.QtCore import QObject


class Worker(QObject):
    progress = pyqtSignal()
