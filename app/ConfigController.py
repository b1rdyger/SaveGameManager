import json
import os
import sys

from PyQt6.QtCore import QFile
from PyQt6.QtDesigner import QFormBuilder
from PyQt6.QtWidgets import QMainWindow


class ConfigController:
    config: dict

    def __init__(self, root_dir, engine):
        self.config_file = f'{root_dir}config{os.sep}games.json'
        self.engine = engine
        if self.check_configfile(self.config_file):
            self.load_config()

    def check_configfile(self, file):
        return bool(os.path.exists(file))

    def load_config(self):
        with open(self.config_file, 'r') as read_content:
            self.config = json.load(read_content)
            self.config['common_save_dir'] = self.get_real_path(self.config['common_save_dir'])
        for one_backup_folder in self.config['backup_save_dirs']:
            one_backup_folder['location'] = self.get_real_path(one_backup_folder['location'])
        for item in self.config.items():
            if item[0].startswith('_'):
                print('Item Ignored')
                continue
            else:
                for value in enumerate(item):
                    print(value)

    # noinspection PyMethodMayBeStatic
    def get_real_path(self, path):
        if os.name == 'nt' and '%USERPROFILE%' in path:
            new_path = os.path.expanduser(os.environ['USERPROFILE'])
            # logger.info(f'{path.replace("%USERPROFILE%", new_path)}')
            return path.replace("%USERPROFILE%", new_path)
        return path


