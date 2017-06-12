"""The search command."""

from paci.helpers import display_helper, cache_helper
from .base import Base


class Search(Base):
    """Searches for a package!"""

    def run(self):
        pkg_name = self.options["<package>"]
        result = cache_helper.find_pkg(pkg_name, self.settings["paci"]["registry"], self.repo_cache)
        if result:
            display_helper.print_list(["Name", "Version", "Description", "Registry"], result)
        else:
            print("Package not found.")
