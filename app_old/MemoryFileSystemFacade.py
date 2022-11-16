import subprocess

from app import EventBus


class Dummy:
    def __call__(self):
        pass


# noinspection PyMethodMayBeStatic
class MemoryFileSystemFacade:
    def __init__(self, save_path, event_bus: EventBus, hidden_tag_file: str):
        self.save_path = save_path
        self.event_bus = event_bus
        self.hidden_tag_file = hidden_tag_file

    # noinspection PyBroadException
    def check_installed(self) -> bool:
        try:
            subprocess.Popen(['imdisk'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    def get_concrete(self):
        if self.check_installed():
            from app.MemoryFileSystem import MemoryFileSystem
            return MemoryFileSystem(self.save_path, self.event_bus, self.hidden_tag_file)
        else:
            return Dummy()
