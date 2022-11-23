import os
import re
import subprocess
import sys
from datetime import datetime

from PyQt6 import uic, QtGui
from PyQt6.QtCore import QThread, pyqtSlot, Qt, QDir
from PyQt6.QtGui import QTextCharFormat, QBrush, QColor, QTextCursor
from PyQt6.QtWidgets import QTextEdit, QApplication

from app.Engine import Engine
from app.LogoffTimerQt import LogoffTimerQt
from app.ProfileSelectorQt import ProfileSelectorQt
from app.SGMSignals.EngineSignals import EngineSignals
from app.SGMSignals.LTSignals import LTSignals
from app.SGMSignals.MFSSignals import MFSSignals
from app.SGMSignals.PCSignals import PCSignals
from app.SGMSignals.SGMSignals import SGMSignals
from app.uiInterfaces.SaveGameManagerUi import SaveGameManagerUi
from app.utils.DateUtils import DateUtils
from app.widgets.MessageByEvent import MessageByEvent


class MyCustomClass(object):
    class SGMTextBrowser(QTextEdit):
        tag = {}
        script_dir = None
        last_message = None
        last_message_counter = 0
        last_cursor_position = None

        def __int__(self, *args):
            QTextEdit.__init__(self, *args)

        def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:# Catch all MouseButtonEvents
            modifiers = QApplication.keyboardModifiers()
            if modifiers == modifiers.KeypadModifier.NoModifier:
                self.moveCursor(QTextCursor.MoveOperation.End)
        def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:# Catch all MouseButtonEvents
            modifiers = QApplication.keyboardModifiers()
            if modifiers == modifiers.KeypadModifier.NoModifier:
                self.moveCursor(QTextCursor.MoveOperation.End)


        def prepare(self, script_dir):
            self.script_dir = script_dir
            regex_search_in_css = '--([a-zA-Z0-9_-]+)\\s*:\\s*(#[a-zA-Z0-9]{3,6});'
            with open(f'{self.script_dir}app{os.sep}widgets{os.sep}tag_colors.css', mode='r') as file:
                tag_colors_css = file.read()
            all_tags = {}
            while found := re.search(regex_search_in_css, tag_colors_css):
                tag_name = found[1]
                tag_color = found[2]
                all_tags[tag_name] = tag_color
                tag_colors_css = tag_colors_css[found.span(0)[1]:]
            for tag, color in all_tags.items():
                self.tag[tag] = QTextCharFormat()
                self.tag[tag].setForeground(QBrush(QColor(color)))
            self.tag['default'] = QTextCharFormat()
            self.tag['default'].setForeground(QBrush(QColor("white")))
            self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            self.setReadOnly(True)
            self.setUndoRedoEnabled(False)

        def write(self, msg, merge_lines=True):
            now = datetime.now().strftime("%H:%M:%S")
            bla = self.textCursor()

            regex_search_in_string = '\\[\[([a-zA-Z0-9]+):(.*?)]]'
            if merge_lines and msg is self.last_message:
                self.last_message_counter += 1
                msg += f' [[info:({self.last_message_counter}x)]]'
                bla = self.textCursor()
                bla.setPosition(self.last_cursor_position, QTextCursor.MoveMode.KeepAnchor)
                self.moveCursor(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.MoveAnchor)
                bla.removeSelectedText()
                self.setTextCursor(bla)
                self.update()
            else:
                self.last_message = msg
                self.last_message_counter = 0

            self.last_cursor_position = self.textCursor().position()
            self.moveCursor(QTextCursor.MoveOperation.End)

            bla.setCharFormat(self.tag['timestamp'])
            bla.insertText(f'[{str(now)}] ')

            while msg != "":
                if matched := re.search(regex_search_in_string, msg):
                    all_start, _ = matched.span(0)
                    sub_msg_start, sub_msg_end = matched.span(2)
                    tag = matched[1]
                    if all_start > 0:
                        bla.setCharFormat(self.tag['default'])
                        bla.insertText(f'{str(msg[:all_start])}')
                        msg = msg[all_start:]
                        sub_msg_start = sub_msg_start - all_start
                        sub_msg_end = sub_msg_end - all_start
                    msg = msg[sub_msg_start:]
                    sub_msg_end -= sub_msg_start
                    bla.setCharFormat(self.tag[tag])
                    bla.insertText(f'{msg[:sub_msg_end]}')
                    msg = msg[sub_msg_end + 2:]
                else:
                    bla.setCharFormat(self.tag['default'])
                    bla.insertText(f'{str(msg)}')
                    break

            bla.insertHtml('<br />')

            self.ensureCursorVisible()


class SaveGameManagerQt(SaveGameManagerUi):
    last_running_state = None

    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir
        self.signals = SGMSignals()
        self.lt_signals = LTSignals()

        # init Engine Thread
        self.engine = Engine(self.root_dir)
        self.engine_thread = QThread()
        self.engine.moveToThread(self.engine_thread)
        self.engine_thread.start()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.config = self.engine.config
        QDir.addSearchPath('icons', self.root_dir + os.sep + 'assets')
        icon = QtGui.QPixmap('icons:arrow_right.png')
        logo = QtGui.QIcon('icons:logo/disk1-256.png')

        # noinspection PyTypeChecker
        sys.modules["MyCustomClass"] = MyCustomClass
        uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'main-window.ui', self)  # Load the .ui file
        self.setWindowIcon(logo)

        self.msg_box.prepare(self.root_dir)
        self.logoff_timer_window = LogoffTimerQt(self.root_dir)
        self.open_profile_selector = ProfileSelectorQt(self.root_dir)

        # self.text_log = self.msg_box()
        self.game_info.setText('')
        self.arrow_up.setPixmap(icon)
        self.arrow_down.setPixmap(icon)
        self.arrow_down.hide()
        self._generate_buttons()

        self.mfs_signals = MFSSignals()
        self.pc_signals = PCSignals()
        self.engine_signals = EngineSignals()
        self.bind_sgm_emits()
        self.bind_lt_emits()
        self.bind_rest_emits()

        self.mbe = MessageByEvent(self.msg_box)
        self.mbe.prepare()

        self.engine.set_write_callback(self.msg_box)
        self.start_engine()
        self.show()

    def _generate_buttons(self):
        # Buttons
        self.btn_start_game.clicked.connect(self.start_dsp)
        self.btn_exit.clicked.connect(self.close)
        self.btn_logoff_timer.clicked.connect(self.open_logoff_timer_window)
        self.action_config.triggered.connect(self.open_profile_selector_window)
        self.action_set_observer_state.triggered.connect(self.set_observer_state)
        self.action_use_ramdrive.triggered.connect(self.set_ramdrive_state)
        self.action_open_savegame_folder.triggered.connect(lambda: os.startfile(self.config['common_save_dir']))
        self.action_exit.triggered.connect(self.close)

    def set_ramdrive_state(self, action: bool):
        self.engine_signals.set_ramdrive_state.emit(action)

    def set_observer_state(self, action: bool):
        self.engine_signals.set_observer_state.emit(action)

    def bind_sgm_emits(self):
        self.signals.run_engine.connect(self.engine.run)
        self.signals.stop_engine.connect(self.engine.stop)

    def bind_lt_emits(self):
        self.lt_signals.timer_set.connect(self.timer_set)
        self.lt_signals.timer_clear.connect(self.timer_clear)

    def bind_rest_emits(self):
        self.mfs_signals.driveCreated.connect(self.ram_disk_mounted)
        self.mfs_signals.driveDestroyed.connect(self.ram_disk_unmounted)
        self.mfs_signals.symlinkCreated.connect(lambda: self.arrow_to_ramdrive(True))
        self.mfs_signals.symlinkRemoved.connect(lambda: self.arrow_to_ramdrive(False))
        self.pc_signals.running.connect(self.change_game_info_panel)
        self.engine_signals.can_be_closed.connect(self.is_cleaned_up)

    def open_profile_selector_window(self):
        self.open_profile_selector.ui.show()

    def open_logoff_timer_window(self):
        self.logoff_timer_window.show()

    @pyqtSlot(datetime)
    def timer_set(self, end_time):
        self.logoff_label.setText(f'Logoff: {DateUtils.get_formated_time(end_time)}')
        self.logoff_label.setStyleSheet('QLabel { background-color : lime; color : black; }')

    @pyqtSlot()
    def timer_clear(self):
        self.logoff_label.setText('Logoff: Off')
        self.logoff_label.setStyleSheet('QLabel { background-color : red; color : black; }')

    @pyqtSlot()
    def arrow_to_ramdrive(self, at_ramdrive):
        if at_ramdrive:
            self.arrow_up.hide()
            self.arrow_down.show()
        else:
            self.arrow_down.hide()
            self.arrow_up.show()

    @pyqtSlot(bool)
    def change_game_info_panel(self, is_running):
        if self.last_running_state == is_running:
            return True
        self.last_running_state = is_running
        if is_running:
            self.game_info.setText('Game Running!')
            self.game_info.setStyleSheet("QLabel { background-color : lime; color : black; }")
            self.btn_start_game.setDisabled(True)
        else:
            self.game_info.setText('Game Stopped!')
            self.game_info.setStyleSheet("QLabel { background-color : red; color : black; }")
            self.btn_start_game.setDisabled(False)

    @pyqtSlot()
    def ram_disk_mounted(self):
        self.memory_save_game.setStyleSheet("QLabel { background-color : lime; color : black; }")

    def ram_disk_unmounted(self):
        self.memory_save_game.setStyleSheet("QLabel { background-color : red; color : black; }")

    def start_engine(self):
        self.signals.run_engine.emit()

    def start_dsp(self):
        subprocess.Popen(f"{self.config['run_cmd']}")

    @staticmethod
    def is_cleaned_up():
        sys.exit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.logoff_timer_window.close()
        self.signals.stop_engine.emit()
