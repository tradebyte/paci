"""The configure command lets you define a settings.yml for paci."""

import os
import json
from paci.helpers import display_helper
from paci.helpers.settings import Settings
from .base import Base


class Configure(Base):
    """Creates a settings.yml for paci interactive with the user."""

    def run(self):
        if not self.options["--no-choice"] and self.options["--silent"]:
            print("Lets configure a new settings.yml for paci!\n")

        settings_helper = Settings()

        # Get standard settings
        std_temp = settings_helper.defaults["paci"]["temp"]
        std_base = settings_helper.defaults["paci"]["base"]
        std_main = settings_helper.defaults["paci"]["registry"]["main"]
        std_fallback = settings_helper.defaults["paci"]["registry"]["fallback"]

        # Handle parameters
        def_main = std_main if not self.options["--main-registry"] else self.options["--main-registry"]
        def_fallback = std_fallback if not self.options["--fallback-registry"] else self.options["--fallback-registry"]

        if self.options["--no-choice"]:
            # Don't ask - use defaults
            if not self.options["--silent"]:
                print("Using defaults.\n")

            temp_dir = std_temp
            base_dir = std_base
            main_registry = def_main
            fallback_registry = def_fallback
        else:
            # Get user input for all values
            temp_dir = display_helper.std_input("Enter directory to store temporary files ({}):\n", std_temp)
            base_dir = display_helper.std_input("Enter file in which to save the package meta data ({}):\n", std_base)
            main_registry = display_helper.std_input("Enter main registry url ({}):\n", def_main)
            fallback_registry = display_helper.std_input("Enter fallback registry url ({}):\n", def_fallback)

        # Create settings dict
        settings = {
            "paci": {
                "temp": os.path.abspath(os.path.expanduser(temp_dir)),
                "base": os.path.abspath(os.path.expanduser(base_dir)),
                "registry": {
                    "main": main_registry,
                    "fallback": fallback_registry
                }
            }
        }

        if self.options["--no-choice"] and not self.options["--silent"]:
            print(json.dumps(settings, indent=4))

        # Save the settings
        settings_helper.write_settings(settings)
