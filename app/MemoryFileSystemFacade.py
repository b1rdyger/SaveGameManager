import subprocess


class Dummy:
    def __call__(self):
        pass


# noinspection PyMethodMayBeStatic
class MemoryFileSystemFacade:
    def __init__(self, save_path, hidden_tag_file: str):
        self.save_path = save_path
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
            return MemoryFileSystem(self.save_path, self.hidden_tag_file)
        else:
            return Dummy()
