import re
import winreg

class CheckRegedit:
    def __init__(self):
        self.software_list = self.search_regedit(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + self.search_regedit(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + self.search_regedit(winreg.HKEY_CURRENT_USER, 0)
        self.found_game()

    def search_regedit(self, hive, flag):
        aReg = winreg.ConnectRegistry(None, hive)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                              0, winreg.KEY_READ | flag)

        count_subkey = winreg.QueryInfoKey(aKey)[0]
        software_list = []

        for i in range(count_subkey):
            software = {}
            try:
                asubkey_name = winreg.EnumKey(aKey, i)
                asubkey = winreg.OpenKey(aKey, asubkey_name)
                if '1366540' in asubkey_name:
                    software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
                    installpath = winreg.QueryValueEx(asubkey, "UninstallString")[0]
                    software['installpath'] = re.search('".*?"', installpath)[0]
                    software_list.append(software)
            except EnvironmentError:
                continue
        return software_list

    def found_game(self):
        if len(self.software_list) == 0:
            return (False, None)
        for software in self.software_list:
            print(f"Name={software['name']}, Version={software['installpath']}")
            return (True, software['installpath'])
