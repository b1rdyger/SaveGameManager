from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtWidgets import QMenuBar

from app.uiInterfaces.QClazzes import QPushButtonClazz, QActionClazz


class SaveGameManagerUi(QMainWindow):
    action_config: QActionClazz
    action_set_observer_state: QActionClazz
    action_use_ramdrive: QActionClazz
    action_open_savegame_folder: QActionClazz
    action_exit: QActionClazz
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
