"""Helper class to deal with the settings.yml"""

import ruamel.yaml
import os

class Settings(object):
    """Helper for managing the paci settings.yml file"""

    def __init__(self, path=None):
        """Initializes the setting path and the default setting values."""
        self.settings = {}

        if path is None:
            self.setting_path = os.environ.get('HOME') + '/.paci/config/settings.yml'
        else:
            self.setting_path = path

        self.defaults = {
            "paci": {
                "temp": "/tmp/paci",
                "index": os.environ.get('HOME') + '/.paci/index.json',
                "base": os.environ.get('HOME') + '/.paci/apps',
                "registry": {
                    "main": "https://raw.githubusercontent.com/tradebyte/paci_packages/master",
                    "fallback": "https://raw.githubusercontent.com/tradebyte/paci_packages/master"
                }
            }
        }

    def fetch_settings(self, path=None):
        """Reads config from a yaml file, using default values if a setting is not defined in the file and returns the resulting settings as a dict."""
        with open(self.setting_path, 'r') as f:
            try:
                # Using defaults, overwriting it with data from the given path
                filesettings = ruamel.yaml.load(f.read(), ruamel.yaml.RoundTripLoader)
            except TypeError:
                print("Provided file '" + self.setting_path + "' is not a valid json file! Using default settings!")
                return self.defaults

        if filesettings is None:
            return self.defaults

        # Merging defaults and settings from file to one dict
        self.settings["paci"] = {**self.defaults["paci"], **filesettings["paci"]}
        self.settings["paci"]["registry"] = {**self.defaults["paci"]["registry"], **filesettings["paci"]["registry"]}

        return self.settings

    def write_settings(self, data):
        """Writes the given data into the settings file"""
        os.makedirs(os.path.dirname(self.setting_path), exist_ok=True)

        with open(self.setting_path, 'w') as f:
            ruamel.yaml.dump(data, stream=f)

    def settings_exist(self):
        """Returns if a setting file exists already"""
        return os.path.isfile(self.setting_path)