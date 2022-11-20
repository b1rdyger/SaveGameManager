import re
import winreg
from dataclasses import dataclass


@dataclass
class GameInfo:
    name: str
    run_cmd: str


class CheckRegedit:
    steam_ids = ['1366540']
    available_games = {}

    def __init__(self):
        self.search_regedit(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
        self.search_regedit(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
        self.search_regedit(winreg.HKEY_CURRENT_USER, 0)

    def search_regedit(self, hive, flag):
        a_reg = winreg.ConnectRegistry(None, hive)
        a_key = winreg.OpenKey(a_reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                               0, winreg.KEY_READ | flag)

        count_subkey = winreg.QueryInfoKey(a_key)[0]

        for i in range(count_subkey):
            try:
                a_subkey_name = winreg.EnumKey(a_key, i)
                a_subkey = winreg.OpenKey(a_key, a_subkey_name)
                for steam_id in self.steam_ids:
                    if steam_id in a_subkey_name:
                        installpath = winreg.QueryValueEx(a_subkey, "UninstallString")[0]
                        software_path = re.search('".*?"', installpath)[0] + ' -applaunch ' + steam_id
                        software_name = winreg.QueryValueEx(a_subkey, "DisplayName")[0]
                        self.available_games[steam_id] = GameInfo(software_name, software_path)
            except EnvironmentError:
                continue
        return self.available_games
