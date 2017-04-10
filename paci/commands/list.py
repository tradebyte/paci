"""The list command."""

from .base import Base
from paci.helpers.pkg_index import PkgIndex
from paci.helpers.settings import Settings


class List(Base):
    """Lists all installed packages!"""

    def run(self):
        settings_helper = Settings()

        if settings_helper.settings_exist() is False:
            print("No packages installed yet!")
            exit(0)

        settings = settings_helper.fetch_settings()
        pkg_db = PkgIndex(settings["paci"]["base"])

        print("Installed packages: \n")

        packages = pkg_db.get_installed()
        col_width = max(len(word) for pkg in packages for word in pkg) + 2
        for pkg in packages:
            print("".join(word.ljust(col_width) for word in pkg))
