"""The list command."""

import os
from paci.helpers import display_helper
from .base import Base


class List(Base):
    """Lists all installed packages!"""

    def run(self):

        if not os.path.exists(self.index_file):
            print("No packages installed yet!")
            exit(1)

        display_helper.print_list(["Name", "Version", "Description"], self.index.get_installed())
