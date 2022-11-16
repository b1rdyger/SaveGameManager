import json
import os
import threading

from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal, QThreadPool

from app.MemoryFileSystemFacade import MemoryFileSystemFacade


# from app.EventBus import EventBus
# from app.FileCopyHero import FileCopyHero, SaveToBlock
# from app.MemoryFileSystemFacade import MemoryFileSystemFacade
# from app.ProcessChecker import ProcessChecker
# from app.SaveGameManager import SaveGameWindow
# from app.global_logging import *
# from app.widgets.ConsoleOutput import ConsoleOutput


class Engine(QRunnable):
    root_dir = None
    config = None
    hidden_tag_file = '.tag-ram'

    def init(self, root_dir, threadpool: QThreadPool, *args, **kwargs):
        # super(Engine, self).__init__()

        self.root_dir = root_dir
        self.threadpool = threadpool

        self.config_file = f'{root_dir}config{os.sep}games.json'
        self.load_config()

        # self._console_output = None

        # self.fch = FileCopyHero(self.event_bus, self.hidden_tag_file, self.config.get('ignored_files'))

        # self.fch.set_from_path(self.config.get('common_save_dir'))

        if not os.path.exists(os.path.join(self.config.get('common_save_dir'))):
            if os.path.islink(os.path.join(self.config.get('common_save_dir'))):
                os.rmdir(self.config.get('common_save_dir'))
            os.mkdir(self.config.get('common_save_dir'))

        backup_folders = self.config.get('backup_save_dirs')

        # for one_backup_folder in backup_folders:
        #     self.fch.add_save_block(SaveToBlock(one_backup_folder['location']))

        # mfs = MemoryFileSystem(self.config.get('common_save_dir'), self.config.get('backup_save_dir')) # @todo
        self.mfs = MemoryFileSystemFacade(self.config.get('common_save_dir'),
                                          self.hidden_tag_file).get_concrete()

        # self.pc = ProcessChecker(self.event_bus, self.config.get('process_name'))

        # self.event_bus.add_listener(SGMStop, self.stop)

    # engine thread
    @pyqtSlot()
    def run(self):
        ram_drive_letter = self.mfs.create_or_just_get()
        os.rmdir(self.config['common_save_dir'])
        if ram_drive_letter is not None:  #and self.fcn.backup_for_symlink():
            self.mfs.create_symlink()
            # self.fch.restore_last_save_from_backup()

        # self._mfs_thread = threading.Thread(target=self.mfs.run).start()
        # fch thread start @todo

    @pyqtSlot()
    def stop(self):
        # alle threads stoppen  @todo
        self.mfs.stop()

    # offer gui console to other modules
    # def set_write_callback(self, co: ConsoleOutput):
        # self.fch.set_console_write_callback(co.write)
        # co.write("Welcome to the [highlighted:SaveGameManager]")

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
