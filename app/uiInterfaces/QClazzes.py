from abc import ABC

from PyQt6.QtCore import pyqtBoundSignal, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QPushButton, QDial, QToolButton


class QPushButtonClazz(QPushButton):
    clicked: pyqtBoundSignal


class QActionClazz(QAction):
    clicked: pyqtBoundSignal
    triggered: pyqtBoundSignal


class QDialClazz(QDial):
    valueChanged: pyqtBoundSignal


class QToolButtonClazz(QToolButton):
    clicked: pyqtBoundSignal
