"""The configure command lets you define a settings.yml for paci."""

import os
from paci.helpers import display_helper
from paci.helpers.settings import Settings
from .base import Base


class Configure(Base):
    """Creates a settings.yml for paci interactive with the user."""

    def run(self):
        print("Lets configure a new settings.yml for paci!\n")
        settings_helper = Settings()

        # get user input for all values
        temp = display_helper.std_input("Enter directory to store temporary files ({}):\n",
                                        settings_helper.defaults["paci"]["temp"])
        base = display_helper.std_input("Enter file in which to save the package meta data ({}):\n",
                                        settings_helper.defaults["paci"]["base"])
        r_main = display_helper.std_input("Enter main registry url ({}):\n",
                                          settings_helper.defaults["paci"]["registry"]["main"])
        r_fallback = display_helper.std_input("Enter fallback registry url ({}):\n",
                                              settings_helper.defaults["paci"]["registry"]["fallback"])

        # create settings dict
        settings = {
            "paci": {
                "temp": os.path.abspath(os.path.expanduser(temp)),
                "base": os.path.abspath(os.path.expanduser(base)),
                "registry": {
                    "main": r_main,
                    "fallback": r_fallback
                }
            }
        }

        # save the settings
        settings_helper.write_settings(settings)
