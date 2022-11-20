import os

from PyQt6.QtCore import pyqtSlot, QObject

from app.ConfigController import ConfigController
from app.FileCopyHero import FileCopyHero, SaveToBlock
from app.MemoryFileSystemFacade import MemoryFileSystemFacade
from app.ProcessChecker import ProcessChecker
from app.SGMSignals.EngineSignals import EngineSignals
from app.SGMSignals.FCHSignals import FCHSignals
from app.SGMSignals.MFSSignals import MFSSignals
from app.ShutdownManager import ShutdownManager


class Engine(QObject):
    root_dir = None
    config = None
    hidden_tag_file = '.tag-ram'
    want_shutdown = False
    mfs = None

    def __init__(self, root_dir):
        super().__init__()

        self.root_dir = root_dir
        self.config = ConfigController(root_dir)
        self.signals = EngineSignals()
        self.fch_signals = FCHSignals()
        self.mfs_signals = MFSSignals()
        self.shutdown_manager = ShutdownManager()

        self.fch = FileCopyHero(self.hidden_tag_file,
                                self.config['ignored_files'], self.config['compressed_save'])
        self.fch.set_from_path(self.config['common_save_dir'])

        backup_folders = self.config['backup_save_dirs']

        for one_backup_folder in backup_folders:
            self.fch.add_save_block(SaveToBlock(one_backup_folder['location']))

        self.pc = ProcessChecker(self.config['process_name'])

        self.fch_signals.backup_successful.connect(self.backup_saved)
        self.signals.want_shutdown.connect(self.set_want_shutdown)

    def set_write_callback(self, msg_box):
        self.fch.set_console_write_callback(msg_box.write)

    def check_save_path(self):
        savegame_path = self.config['common_save_dir']
        self.signals.check_safegame_folder.emit(savegame_path)

        if not os.path.isdir(savegame_path):
            self.mfs_signals.folder_not_found.emit(savegame_path)
            if os.path.islink(savegame_path):
                self.fch_signals.broken_link.emit(savegame_path)
                os.rmdir(savegame_path)
            os.mkdir(savegame_path)
        self.signals.folder_found.emit(savegame_path)

    @pyqtSlot()
    def backup_saved(self):
        if self.want_shutdown:
            self.signals.shutdown_allowed.emit()

    @pyqtSlot(bool)
    def set_want_shutdown(self, var):
        self.want_shutdown = var

    # engine thread
    @pyqtSlot()
    def run(self):
        self.signals.engine_started.emit()
        self.check_save_path()
        self.mfs = MemoryFileSystemFacade(self.config['common_save_dir'],
                                          self.hidden_tag_file).get_concrete()
        ram_drive_letter = self.mfs.create_or_just_get()
        if ram_drive_letter is not None and self.fch.backup_for_symlink() and self.mfs.create_symlink():
            self.fch.restore_last_save_from_backup()
        self.fch.start_observer()

    @pyqtSlot()
    def stop(self):
        self.fch.stop_observer()
        if self.mfs:
            self.mfs.stop()

    def load_profile(self):
        self.profiles = self.config['profiles']




