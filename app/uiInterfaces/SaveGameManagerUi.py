from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QMenuBar
from PyQt6.QtWidgets import QMainWindow, QLabel
from app.uiInterfaces.QClazzes import QPushButtonClazz


class SaveGameManagerUi(QMainWindow):
    menubar: QMenuBar
    logoff_label: QLabel
    game_info: QLabel
    arrow_up: QLabel
    arrow_down: QLabel
    btn_logoff_timer: QPushButtonClazz
    btn_exit: QPushButtonClazz
    btn_start_game: QPushButtonClazz
    msg_box = None
    game_info: QLabel
    memory_save_game: QLabel
    default_save_game: QLabel  # RamDisk ready
    backup_label: QLabel
