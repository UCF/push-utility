import json
import io

class Settings:
    settings_dict = None

    def read_file():
        with open('settings.json', 'r') as settings_file:
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
        with open('settings.json', 'w') as setting_file:
            json.dump(setting_args, setting_file)
