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

        if not os.path.isdir(self.config.get('common_save_dir')):#TODO: Hier können keine EMITS durchgeführt werden wenn z.B. der Ornder Save fehlt
            if os.path.islink(self.config.get('common_save_dir')):
                os.rmdir(self.config.get('common_save_dir'))
            os.mkdir(self.config.get('common_save_dir'))

        backup_folders = self.config.get('backup_save_dirs')

        for one_backup_folder in backup_folders:
            self.fch.add_save_block(SaveToBlock(one_backup_folder['location']))

        self.mfs = MemoryFileSystemFacade(self.config.get('common_save_dir'),
                                          self.hidden_tag_file).get_concrete()

        self.pc = ProcessChecker(self.config.get('process_name'))

        self.fch_signals.backup_successful.connect(self.backup_saved)

    def set_write_callback(self, msg_box):
        self.fch.set_console_write_callback(msg_box.write)

    @pyqtSlot()
    def backup_saved(self):
        if self.want_shutdown:
            self.signals.shutdown_allowed.emit()

    # engine thread
    @pyqtSlot()
    def run(self):
        ram_drive_letter = self.mfs.create_or_just_get()
        if ram_drive_letter is not None and self.fch.backup_for_symlink() and self.mfs.create_symlink():
            self.fch.restore_last_save_from_backup()
        self.fch.start_observer()

    @pyqtSlot()
    def stop(self):
        self.fch.stop_observer()
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


