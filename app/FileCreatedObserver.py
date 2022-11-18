import logging

from PyQt6.QtCore import QObject, pyqtSlot
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileCreatedObserver(QObject):

    def __init__(self, file_created_callback, ignored_files_list):
        super().__init__()
        self.my_event_handler = Handler(file_created_callback, ignored_files_list)
        self.my_observer = None
        self.path = None

    @pyqtSlot(str)
    def start(self, path):
        if self.my_observer:
            self.stop()
            self.path = None
        self.my_observer = Observer()
        try:
            self.my_observer.schedule(self.my_event_handler, path=path, recursive=False)
            self.path = path
        except Exception as e:
            logging.exception(e)
        try:
            self.my_observer.start()
        except Exception as e:
            logging.exception(e)

    @pyqtSlot()
    def stop(self):
        self.my_observer.stop()


class Handler(FileSystemEventHandler):

    def __init__(self, file_created_callback, ignored_files_list):
        self.file_created_callback = file_created_callback
        self.ignored_files_list = ignored_files_list

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            filename = event.src_path.split('\\')[-1]
            if filename not in self.ignored_files_list:
                self.file_created_callback()
