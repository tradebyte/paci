# -*- coding: utf-8 -*-
"""The base command."""

import os
from paci.helpers.settings import Settings
from paci.helpers.pkg_index import PkgIndex


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        """Initialize the all globally available constants."""

        self.options = options
        self.args = args
        self.kwargs = kwargs

        if not options["configure"]:
            settings_helper = Settings()

            if settings_helper.settings_exist() is False:
                settings_helper.write_settings(settings_helper.defaults)

            # Define global variables
            self.settings = settings_helper.fetch_settings()
            self.repo_cache = os.path.join(self.settings["paci"]["base"], "cache")
            self.base_pkg_dir = os.path.join(self.settings["paci"]["base"], "apps")
            self.index_file = os.path.join(self.settings["paci"]["base"], "pkgs.json")
            self.index = PkgIndex(self.index_file)

            # Ensure the directories are present
            os.makedirs(self.repo_cache, exist_ok=True)
            os.makedirs(self.base_pkg_dir, exist_ok=True)
            os.makedirs(self.settings["paci"]["temp"], exist_ok=True)

    def run(self):
        """Acts as an interface for all commands. This is where your logic goes."""
        raise NotImplementedError("You must implement the run() method yourself!")
