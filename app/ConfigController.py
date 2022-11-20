import json
import os


class ConfigController:
    def __init__(self, root_dir, engine):
        self.config_file = f'{root_dir}config{os.sep}games.json'
        self.engine = engine
        self.load_config()

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
