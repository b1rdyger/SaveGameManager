from PyQt6.QtCore import QObject

from app.utils.PyQtSingleton import PyQtSingleton


class SGMSignalObjects(QObject, metaclass=PyQtSingleton):
    pass
