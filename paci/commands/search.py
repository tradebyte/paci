"""The search command."""

from paci.helpers import display_helper, cache_helper, std_helper
from termcolor import colored
from .base import Base


class Search(Base):
    """Searches for a package!"""

    def run(self):
        pkg_name = self.options["<package>"]
        result = cache_helper.find_pkg(pkg_name, self.settings["paci"]["registry"], self.repo_cache)
        if result:
            print(colored("Showing all search results for \"{}\"...\n".format(std_helper.stringify(pkg_name)), 'yellow', attrs=['bold']))
            display_helper.print_list(["Name", "Version", "Description", "Registry"], result)
        else:
            print("Package not found.")
