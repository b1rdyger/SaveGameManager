from PyQt6.QtWidgets import QWidget, QDial, QPushButton, QLabel, QLCDNumber

from app.uiInterfaces.SaveGameManagerUi import SaveGameManagerUi


class LogoffTimerUi(QWidget):
    parent: SaveGameManagerUi
    logoff_time_status: QLabel
    logoff_dial: QDial
    logoff_time_status: QLabel
    btn_set_timer: QPushButton
    btn_cancel_timer: QPushButton
    btn_quit_timer: QPushButton
    logoff_ic: QLCDNumber
