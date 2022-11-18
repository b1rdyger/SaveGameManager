import os
import re
import subprocess
import sys
from datetime import datetime

from PyQt6 import uic, QtCore, QtGui
from PyQt6.QtCore import QThread, pyqtSlot
from PyQt6.QtGui import QTextCharFormat, QBrush, QColor
from PyQt6.QtWidgets import QTextEdit

from app.Engine import Engine
from app.LogoffTimerQt import LogoffTimerQt
from app.SGMSignals.MFSSignals import MFSSignals
from app.SGMSignals.PCSignals import PCSignals
from app.SGMSignals.SGMSignals import SGMSignals
from app.uiInterfaces.SaveGameManagerUi import SaveGameManagerUi
from app.widgets.MessageByEvent import MessageByEvent


class MyCustomClass(object):
    class SGMTextBrowser(QTextEdit):
        tag = {}
        script_dir = None

        def __int__(self, *args):
            QTextEdit.__init__(self, *args)
            self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
            self.setReadOnly(True)
            self.setUndoRedoEnabled(False)

        def prepare(self, script_dir):
            self.script_dir = script_dir
            with open(f'{self.script_dir}app{os.sep}widgets{os.sep}tag_colors.css', mode='r') as file:
                tag_colors_css = file.read()
            all_tags = {}
            while found := re.search('--([a-zA-Z0-9_-]+)\\s*:\\s*(#[a-zA-Z0-9]{3,6});', tag_colors_css):
                tag_name = found[1]
                tag_color = found[2]
                all_tags[tag_name] = tag_color
                tag_colors_css = tag_colors_css[found.span(0)[1]:]
            for tag, color in all_tags.items():
                self.tag[tag] = QTextCharFormat()
                self.tag[tag].setForeground(QBrush(QColor(color)))

            self.tag['default'] = QTextCharFormat()
            self.tag['default'].setForeground(QBrush(QColor("white")))

        def write(self, msg):
            now = datetime.now().strftime("%H:%M:%S")
            bla = self.textCursor()
            bla.setCharFormat(self.tag['timestamp'])
            bla.insertText(f'[{str(now)}] ')

            while msg != "":
                if matched := re.search('\\[([a-zA-Z0-9]+):(.*?)]', msg):
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
                    msg = msg[sub_msg_end + 1:]
                else:
                    bla.setCharFormat(self.tag['default'])
                    bla.insertText(f'{str(msg)}')
                    break
            bla.insertHtml('<br />')

            # self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
            self.ensureCursorVisible()


class SaveGameManagerQt(SaveGameManagerUi):
    last_running_state = None

    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir
        self.signals = SGMSignals()

        # init Engine Thread
        self.engine = Engine(self.root_dir)
        self.engine_thread = QThread()
        self.engine.moveToThread(self.engine_thread)
        self.engine_thread.start()

        self.config = self.engine.config
        QtCore.QDir.addSearchPath('icons', self.root_dir + os.sep + 'assets')
        icon = QtGui.QPixmap('icons:arrow_right.png')
        logo = QtGui.QIcon('icons:logo/disk1-256.png')

        # noinspection PyTypeChecker
        sys.modules["MyCustomClass"] = MyCustomClass
        uic.loadUi(self.root_dir + os.sep + 'assets' + os.sep + 'main-window.ui', self)  # Load the .ui file
        self.setWindowIcon(logo)

        self.msg_box.prepare(self.root_dir)
        self.new_window = LogoffTimerQt(self.root_dir)

        # self.text_log = self.msg_box()
        self.game_info.setText('')
        self.arrow_up.setPixmap(icon)
        self.arrow_down.setPixmap(icon)
        self.arrow_down.hide()
        self.show()  # Show the GUI
        self._generate_buttons()

        self.mfs_signals = MFSSignals()
        self.pc_signals = PCSignals()
        self.bind_engine_emits()
        self.bind_mfs_emits()

        self.mbe = MessageByEvent(self.msg_box)
        self.mbe.prepare()

        self.start_engine()

    def _generate_buttons(self):
        # Buttons
        self.btn_start_game.clicked.connect(self.start_dsp)
        self.btn_exit.clicked.connect(self.exit)
        self.btn_logoff_timer.clicked.connect(self.open_logoff_timer_window)

    def bind_engine_emits(self):
        self.signals.run_engine.connect(self.engine.run)
        self.signals.stop_engine.connect(self.engine.stop)

    def bind_mfs_emits(self):
        self.mfs_signals.cleanedUp.connect(self.close)
        self.mfs_signals.driveCreated.connect(self.ram_disk_mounted)
        self.mfs_signals.symlinkCreated.connect(lambda: self.arrow_to_ramdrive(True))
        self.mfs_signals.symlinkRemoved.connect(lambda: self.arrow_to_ramdrive(False))
        self.pc_signals.running.connect(self.change_game_info_panel)

    def open_logoff_timer_window(self):
        self.new_window.show()

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

    def start_engine(self):
        self.signals.run_engine.emit()

    def start_dsp(self):
        subprocess.Popen(rf"{self.config.get('steam_path')} -applaunch 1366540")

    def exit(self):
        self.signals.stop_engine.emit()
