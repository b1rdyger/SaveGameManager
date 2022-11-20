import json
import os
import re


from app.CheckRegedit import CheckRegedit, GameInfo


class ConfigController:
    config: json

    def __init__(self, root_dir):
        self.config_file = f'{root_dir}config{os.sep}games.json'
        if not self.__load_config(self.config_file):
            raise FileNotFoundError('Config file could not be loaded')

        check_regedit = CheckRegedit()
        for profile in self.config.get('profiles'):
            self.__fix_directories(profile)
            self.__fix_run_cmd(profile, check_regedit)

    def __getitem__(self, profile, item):
        return self.config.get(profile).get(item)

    def __load_config(self, file) -> bool:
        if bool(os.path.exists(file)):
            with open(self.config_file, 'r') as read_content:
                self.config = json.load(read_content)
                return True
        return False

    def __fix_run_cmd(self, sub_config, regedit):
        sub_item = self.config.get('profiles').get(sub_config)
        run_cmd = sub_item.get('run_cmd')
        if run_id_match := re.search('^id:([0-9]+)$', run_cmd):
            run_id = run_id_match[1]
            if run_id in regedit.available_games:
                game_info: GameInfo = regedit.available_games[run_id]
                sub_item['run_cmd'] = game_info.run_cmd

    def __fix_directories(self, sub_config):
        sub_item = self.config.get('profiles').get(sub_config)
        sub_item['common_save_dir'] = self.__get_real_path(sub_item['common_save_dir'])
        for one_backup_folder in sub_item['backup_save_dirs']:
            one_backup_folder['location'] = self.__get_real_path(one_backup_folder['location'])

    # noinspection PyMethodMayBeStatic
    def __get_real_path(self, path):
        if os.name == 'nt' and '%USERPROFILE%' in path:
            new_path = os.path.expanduser(os.environ['USERPROFILE'])
            return path.replace("%USERPROFILE%", new_path)
        return path
