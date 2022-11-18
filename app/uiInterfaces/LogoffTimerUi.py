from PyQt6.QtWidgets import QWidget, QDial, QPushButton, QLabel, QLCDNumber


class LogoffTimerUi(QWidget):
    logoff_dial: QDial
    logoff_time_status: QLabel
    btn_set_timer: QPushButton
    btn_cancel_timer: QPushButton
    logoff_ic: QLCDNumber
