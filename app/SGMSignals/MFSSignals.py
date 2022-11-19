from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class MFSSignals(SGMSignalObjects):

    driveCreated = pyqtSignal(str)
    driveDestroyed = pyqtSignal()
    savePathNotEmpty = pyqtSignal()
    savePathDoesNotExists = pyqtSignal()
    symlinkCreated = pyqtSignal()
    symlinkRemoved = pyqtSignal()
    cleanedUp = pyqtSignal()
    folder_not_empty = pyqtSignal(str)
    folder_not_found = pyqtSignal(str)
    folder_created = pyqtSignal(str)