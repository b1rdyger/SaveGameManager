import json
import os

from PyQt6.QtCore import pyqtSlot, QObject

from app.FileCopyHero import FileCopyHero, SaveToBlock
from app.MemoryFileSystemFacade import MemoryFileSystemFacade
from app.ProcessChecker import ProcessChecker
from app.SGMSignals.EngineSignals import EngineSignals
from app.SGMSignals.FCHSignals import FCHSignals
from app.SGMSignals.MFSSignals import MFSSignals


class Engine(QObject):
    root_dir = None
    config = None
    hidden_tag_file = '.tag-ram'
    want_shutdown = False
    mfs = None

    def __init__(self, root_dir):
        super().__init__()

        self.root_dir = root_dir

        self.config_file = f'{root_dir}config{os.sep}games.json'
        self.load_config()

        self.signals = EngineSignals()
        self.fch_signals = FCHSignals()
        self.mfs_signals = MFSSignals()
        self.fch = FileCopyHero(self.hidden_tag_file,
                                self.config.get('ignored_files'), self.config.get('compressed_save'))
        self.fch.set_from_path(self.config.get('common_save_dir'))

        backup_folders = self.config.get('backup_save_dirs')

        for one_backup_folder in backup_folders:
            self.fch.add_save_block(SaveToBlock(one_backup_folder['location']))

        self.pc = ProcessChecker(self.config.get('process_name'))

        self.fch_signals.backup_successful.connect(self.backup_saved)

    def set_write_callback(self, msg_box):
        self.fch.set_console_write_callback(msg_box.write)

    def check_save_path(self):
        savegame_path = self.config.get('common_save_dir')
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

    # engine thread
    @pyqtSlot()
    def run(self):
        self.signals.engine_started.emit()
        self.check_save_path()
        self.mfs = MemoryFileSystemFacade(self.config.get('common_save_dir'),
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
        profiles = self.config.get('profiles')

    def load_config(self):
        with open(self.config_file, 'r') as read_content:
            self.config = json.load(read_content)
            self.config['common_save_dir'] = self.get_real_path(self.config['common_save_dir'])
        for one_backup_folder in self.config['backup_save_dirs']:
            one_backup_folder['location'] = self.get_real_path(one_backup_folder['location'])

    # noinspection PyMethodMayBeStatic
    def get_real_path(self, path):
        if os.name == 'nt' and '%USERPROFILE%' in path:
            new_path = os.path.expanduser(os.environ['USERPROFILE'])
            # logger.info(f'{path.replace("%USERPROFILE%", new_path)}')
            return path.replace("%USERPROFILE%", new_path)
        return path


