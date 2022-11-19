from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton


class SaveGameManagerUi(QMainWindow):
    logoff_label: QLabel
    game_info: QLabel
    arrow_up: QLabel
    arrow_down: QLabel
    btn_logoff_timer: QPushButton
    btn_exit: QPushButton
    btn_start_game: QPushButton
    msg_box = None
    game_info: QLabel
    memory_save_game: QLabel
    default_save_game: QLabel  # RamDisk ready
    backup_label: QLabel
