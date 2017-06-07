"""Helper class to deal with the settings.yml"""

import ruamel.yaml
import os


class Settings(object):
    """Helper for managing the paci settings.yml file"""

    def __init__(self):
        """Initializes the setting path and the default setting values."""
        self.settings = {}
        self.setting_path = os.path.join(os.environ.get("HOME"), ".config/paci/settings.yml")
        self.defaults = {
            "paci": {
                "temp": "/tmp/paci",
                "base": os.path.join(os.environ.get("HOME"), ".paci"),
                "registry": {
                    "main": "https://raw.githubusercontent.com/tradebyte/paci_packages/master",
                    "fallback": "https://raw.githubusercontent.com/tradebyte/paci_packages/master"
                }
            }
        }

    def fetch_settings(self):
        """
            Reads config from a yaml file, using default values if a setting is not defined
            in the file and returns the resulting settings as a dict.
        """
        with open(self.setting_path, "r") as f:
            try:
                # Using defaults, overwriting it with data from the given path
                settings_file = ruamel.yaml.load(f.read(), ruamel.yaml.RoundTripLoader)
            except TypeError:
                print("Provided file {} is not a valid json file! Using default settings!".format(self.setting_path))
                return self.defaults

        if settings_file is None:
            return self.defaults

        # Merging defaults and settings from file to one dict
        self.settings["paci"] = {**self.defaults["paci"], **settings_file["paci"]}
        self.settings["paci"]["registry"] = {**self.defaults["paci"]["registry"], **settings_file["paci"]["registry"]}

        # Ensure the base directory exists
        os.makedirs(os.path.dirname(self.settings["paci"]["base"]), exist_ok=True)

        return self.settings

    def write_settings(self, data):
        """Writes the given data into the settings file"""
        os.makedirs(os.path.dirname(self.setting_path), exist_ok=True)

        try:
            with open(self.setting_path, "w") as f:
                ruamel.yaml.dump(data, stream=f)
        except IOError as e:
            print("Couldn't open or write to file (%s)." % e)

    def settings_exist(self):
        """Returns if a setting file exists already"""
        return os.path.isfile(self.setting_path)
