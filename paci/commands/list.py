"""The list command."""

import os
from paci.helpers import display_helper, cache_helper
from termcolor import colored
from .base import Base


class List(Base):
    """Lists packages!"""

    def run(self):

        # List all installed packages
        if self.options["--installed"]:
            if not os.path.exists(self.index_file):
                print("No packages installed yet!")
                exit(1)

            print(colored("Displaying all installed packages...\n", 'yellow', attrs=['bold']))
            display_helper.print_list(["Name", "Version", "Description"], self.index.get_installed())

        # List all available packages
        if not self.options["--installed"]:
            print(colored("Displaying all available packages...\n", 'yellow', attrs=['bold']))

            result = cache_helper.get_pkgs(self.settings["paci"]["registry"], self.repo_cache)
            if result:
                display_helper.print_list(["Name", "Version", "Description", "Registry"], result)
