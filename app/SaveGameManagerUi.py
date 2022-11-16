from PyQt6.QtWidgets import QMainWindow, QLabel


class SaveGameManagerUi(QMainWindow):
    arrow: QLabel
    btn_logoff_timer = None
    btn_exit = None
    btn_start_game = None
    msg_box = None
