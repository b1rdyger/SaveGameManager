from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtWidgets import QPushButton, QDial


class QPushButtonClazz(QPushButton):
    clicked: pyqtBoundSignal


class QDialClazz(QDial):
    valueChanged: pyqtBoundSignal
