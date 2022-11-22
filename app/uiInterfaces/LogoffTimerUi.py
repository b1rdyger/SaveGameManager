from PyQt6.QtWidgets import QWidget, QLabel, QLCDNumber

from app.uiInterfaces.QClazzes import QPushButtonClazz, QDialClazz
from app.uiInterfaces.SaveGameManagerUi import SaveGameManagerUi


class LogoffTimerUi(QWidget):
    parent: SaveGameManagerUi
    logoff_time_status: QLabel
    logoff_dial: QDialClazz
    logoff_time_status: QLabel
    btn_set_timer: QPushButtonClazz
    btn_cancel_timer: QPushButtonClazz
    btn_quit_timer: QPushButtonClazz
    logoff_ic: QLCDNumber
    btn_test_function: QPushButtonClazz
