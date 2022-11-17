from PyQt6.QtCore import pyqtSignal

from app.SGMSignals._SGMSignalObjects import SGMSignalObjects


class MFSSignals(SGMSignalObjects):

    driveCreated = pyqtSignal()
    driveDestroyed = pyqtSignal()
    savePathNotEmpty = pyqtSignal()
    savePathDoesNotExists = pyqtSignal()
    symlinkCreated = pyqtSignal()
    symlinkRemoved = pyqtSignal()

    cleanedUp = pyqtSignal()
