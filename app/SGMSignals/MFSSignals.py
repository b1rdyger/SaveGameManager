from PyQt6.QtCore import QObject, pyqtSignal


class MFSSignals(QObject):

    driveCreated = pyqtSignal()
    driveDestroyed = pyqtSignal()
    savePathNotEmpty = pyqtSignal()
    savePathDoesNotExists = pyqtSignal()
    symlinkCreated = pyqtSignal()
    symlinkRemoved = pyqtSignal()

