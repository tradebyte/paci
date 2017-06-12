"""The refresh command."""

import os
from paci.helpers import download_helper
from .base import Base


class Refresh(Base):
    """Refreshes the repo sources list!"""

    def run(self):
        for repo in self.settings["paci"]["registry"]:
            url = os.path.join(self.settings["paci"]["registry"][repo], "index.json")
            download_helper.download(url, self.repo_cache, filename="{}.json".format(repo))

        print("\nRefreshing of the package repos complete.")
