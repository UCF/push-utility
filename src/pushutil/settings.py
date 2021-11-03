import os
import json
from pathlib import Path

class Settings:
    settings_dict = None

    def get_file_path() -> str:
        homedir = Path.home()
        return os.path.join(homedir, '.ucfpushutil.json')

    def read_file():
        homedir = Path.home()
        with open(Settings.get_file_path(), 'r') as settings_file:
            Settings.settings_dict = json.load(settings_file)

    @classmethod
    def get_setting(self, setting_name):
        if not setting_name:
            return None

        if Settings.settings_dict == None:
            self.read_file()

        if setting_name in self.settings_dict.keys():
            return self.settings_dict[setting_name]
        else:
            return None

    def write_settings(setting_args):
        with open(Settings.get_file_path(), 'w') as setting_file:
            json.dump(setting_args, setting_file)
