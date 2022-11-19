import glob
import logging
import os
import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

from PyQt6.QtCore import QThread

from app.FileCreatedObserver import FileCreatedObserver
from app.SGMSignals.FCHSignals import FCHSignals


@dataclass
class SaveToBlock:
    path: Path
    cap_number: int = 0
    cap_size_mb: int = 0
    tpe: str = 'auto'


class FileCopyHero:

    save_from: str = None
    save_to_list: list[SaveToBlock] = []
    log: callable = None
    last_saved_or_restored_filename: str = None

    def __init__(self, hidden_tag_file, ignored_files, compressed_save):
        self.hidden_tag_file = hidden_tag_file
        self.ignored_files = ignored_files
        self.compressed_save = compressed_save

        self.signals = FCHSignals()

        self.fco = FileCreatedObserver(self.callback_file_created)
        self.fco_thread = QThread()
        self.fco.moveToThread(self.fco_thread)
        self.fco_thread.start()
        self.bind_engine_emits()

    def bind_engine_emits(self):
        self.signals.start_observer.connect(self.fco.start)
        self.signals.stop_observer.connect(self.fco.stop)

    def set_console_write_callback(self, write_callback: callable):
        self.log = write_callback

    def console_log(self, txt: str):
        if self.log:
            self.log(txt)
        else:
            logging.info(txt)

    def set_from_path(self, save_from: str):
        self.save_from = fr'{save_from}'

    def start_observer(self):
        self.signals.start_observer.emit(self.save_from)

    def stop_observer(self):
        self.signals.stop_observer.emit()

    def add_save_block(self, save_to: SaveToBlock):
        self.save_to_list.append(save_to)

    # just save everything everywhere without worrying about the config
    def full_backup(self):
        self.console_log('Full backup')
        files_in_save = os.listdir(self.save_from)
        if files_in_save not in [None, '']:
            self.backup_files(files_in_save)

    def callback_file_created(self, filename: str):
        is_ignored = len([i for i in [re.search(x, filename) for x in self.ignored_files] if i is not None]) > 0
        if filename.startswith('[Recovery]-'):
            self.restore_last_save_from_backup(True, filename)
        if not is_ignored:
            self.smart_backup()

    # save everything everywhere according to the configuration
    def smart_backup(self, tryy=0) -> bool:
        if tryy == 5:
            self.signals.backup_fails.emit()
            return True
        if tryy == 0:
            self.signals.backup_start.emit()
        files_in_save = os.listdir(self.save_from)
        if files_in_save not in [None, '']:
            # @todo get cluster, config, log_rotate
            try:
                self.backup_files(files_in_save)
                self.signals.smart_backup_finished.emit()
                self.signals.backup_successful.emit()
            except Exception:
                time.sleep(0.2 + (2**tryy)/10)
                self.smart_backup(tryy+1)

    # noinspection PyTypeChecker
    def restore_last_save_from_backup(self, exclude_observer=False, filename=None) -> bool:
        first_backup_block = next(iter(self.save_to_list or []), None)
        if not first_backup_block:
            return False
        files = list(filter(os.path.isfile, glob.glob(str(first_backup_block.path) + "\\*")))
        files = list(map(lambda f: {'file': f, 'mtime': os.path.getmtime(f)}, files))
        files = sorted(files, key=lambda d: d['mtime'], reverse=True)
        split_dt = 59
        dts = (d0['mtime']-d1['mtime'] for d0, d1 in zip(files, files[1:]))
        split_at = [i for i, dt in enumerate(dts, 1) if dt >= split_dt]
        groups = [files[i:j] for i, j in zip([0]+split_at, split_at+[None])]
        if exclude_observer:
            self.signals.start_rename.emit()
        for savegame in groups[0]:
            savegame_filename_only = savegame['file'].split('\\')[-1]
            try:
                if exclude_observer:
                    if filename.__contains__(savegame_filename_only):
                        while self.is_file_in_use(f'{self.save_from}{os.sep}{savegame_filename_only}'):
                            # self.console_log(f'[error: File "{savegame_filename_only}"] in use, waiting')
                            self.signals.cannot_use.emit(savegame_filename_only)
                            time.sleep(0.1)
                        os.remove(f'{self.save_from}{os.sep}{savegame_filename_only}')
                        self.last_saved_or_restored_filename = f'{savegame_filename_only}'
                        self.signals.renamed.emit(self.last_saved_or_restored_filename) #TODO: fix me, "]" wird falsch interpretiert!!
                        continue
                    else:
                        os.rename(f'{self.save_from}{os.sep}{savegame_filename_only}', f'{self.save_from}{os.sep}[Recovery]-{savegame_filename_only}')
                        self.last_saved_or_restored_filename = f'[Recovery]-{savegame_filename_only}' #TODO: fix me, "]" wird falsch interpretiert!!
                        self.signals.renamed.emit(self.last_saved_or_restored_filename)
                else:
                    shutil.copy2(f'{savegame["file"]}', f'{self.save_from}')
                    self.last_saved_or_restored_filename = savegame_filename_only
                    self.signals.restored.emit(savegame_filename_only)
            except Exception as e:

                self.signals.not_restored.emit(savegame_filename_only)
                logging.exception(e)

    def backup_files(self, files: list[str]):
        for save_to in self.save_to_list:
            if not os.path.isdir(save_to.path):
                self.signals.folder_not_found.emit(save_to.path)
                os.mkdir(save_to.path)
                self.signals.folder_created.emit(save_to.path)
            for file in files:
                if self.hidden_tag_file not in file:
                    while self.is_file_in_use(f'{self.save_from}{os.sep}{file}'):
                        self.signals.cannot_use.emit(file)
                        time.sleep(0.1)
                    shutil.copy2(f'{self.save_from}{os.sep}{file}', f'{save_to.path}')
                    while self.is_file_in_use(f'{self.save_from}{os.sep}{file}'):
                        self.signals.cannot_use.emit(file)
                        time.sleep(0.1)
                    os.remove(f'{self.save_from}{os.sep}{file}')
                    self.console_log(f'[highlighted:Smart backup {file}]')


    def backup_for_symlink(self) -> bool:
        first_backup_path = next(iter(self.save_to_list or []), None)
        if first_backup_path is None:
            return False
        else:
            first_backup_path = first_backup_path.path
        if os.path.isdir(self.save_from):
            if not os.path.isdir(first_backup_path):
                self.signals.folder_not_found.emit(first_backup_path)
                os.mkdir(first_backup_path)
                self.signals.folder_created.emit(first_backup_path)
            files_in_save = os.listdir(self.save_from)
            if files_in_save not in [None, '']:
                for file_name in files_in_save:
                    if file_name != self.hidden_tag_file:
                        while self.is_file_in_use(f'{self.save_from}{os.sep}{file_name}'):
                            self.signals.cannot_use.emit(file_name)
                            time.sleep(0.1)
                        shutil.copy2(os.path.join(self.save_from, file_name), first_backup_path)
                        while self.is_file_in_use(f'{self.save_from}{os.sep}{file_name}'):
                            self.signals.cannot_use.emit(file_name)
                            time.sleep(0.1)
                        os.remove(os.path.join(self.save_from, file_name))
                os.rmdir(self.save_from)
            return True
        return False

    def is_file_in_use(self, file_path):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError

        try:
            path.rename(path)
        except PermissionError:
            return True
        else:
            return False
