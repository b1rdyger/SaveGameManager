import json
import os
import re


from app.CheckRegedit import CheckRegedit, GameInfo


class ConfigController:
    config: dict

    def __init__(self, root_dir, engine):
        self.config_file = f'{root_dir}config{os.sep}games.json'
        self.engine = engine
        if self.__check_configfile(self.config_file):
            self.__load_config()
        check_regedit = CheckRegedit()
        run_cmd = self.config.get('run_cmd')
        if run_id_match := re.search('^id:([0-9]+)$', run_cmd):
            run_id = run_id_match[1]
            if run_id in check_regedit.available_games:
                game_info: GameInfo = check_regedit.available_games[run_id]
                self.config['run_cmd'] = game_info.run_cmd

    def __getitem__(self, item):
        return self.config.get(item)

    @staticmethod
    def __check_configfile(file):
        return bool(os.path.exists(file))

    def __load_config(self):
        with open(self.config_file, 'r') as read_content:
            self.config = json.load(read_content)
            self.config['common_save_dir'] = self.__get_real_path(self.config['common_save_dir'])
        for one_backup_folder in self.config['backup_save_dirs']:
            one_backup_folder['location'] = self.__get_real_path(one_backup_folder['location'])
        for item in self.config.items():
            if item[0].startswith('_'):
                print('Item Ignored')
                continue
            else:
                for value in enumerate(item):
                    print(value)

    # noinspection PyMethodMayBeStatic
    def __get_real_path(self, path):
        if os.name == 'nt' and '%USERPROFILE%' in path:
            new_path = os.path.expanduser(os.environ['USERPROFILE'])
            # logger.info(f'{path.replace("%USERPROFILE%", new_path)}')
            return path.replace("%USERPROFILE%", new_path)
        return path


