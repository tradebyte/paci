"""The list command."""

import os
from .base import Base
from paci.helpers import display_helper


class List(Base):
    """Lists all installed packages!"""

    def run(self):

        if not os.path.exists(self.index_file):
            print("No packages installed yet!")
            exit(1)

        display_helper.print_list(["Name", "Version", "Description"], self.index.get_installed())

