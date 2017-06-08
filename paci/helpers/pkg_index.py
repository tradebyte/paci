"""Helper to deal with the index.json"""

from tinydb import *
from paci.helpers import std_helper


class PkgIndex(object):
    """Helper for managing the packages index.json file"""

    def __init__(self, path):
        """Initializes the setting path and the default setting values."""
        self.db = TinyDB(path, create_dirs=True)

    def add(self, pkg):
        """Safely adds a new record to pkg index list."""
        query = Query()

        # Create
        if not self.db.search(query.name == pkg["pkg_name"]):
            self.db.insert({"name": pkg["pkg_name"],
                            "ver": pkg["pkg_ver"],
                            "desc": pkg["pkg_desc"]
                            })
        # Update
        elif self.db.search((query.name == pkg["pkg_name"]) & (query.ver != pkg["pkg_ver"])):
            self.db.update(self.__update_record(pkg), query.name == pkg["pkg_name"])

    def get_installed(self):
        """Gets a list of installed packages."""
        pkgs = []
        for pkg in self.db.all():
            pkgs.append([pkg["name"], pkg["ver"], pkg["desc"]])
        return pkgs

    def get_pkg(self, pkg_name):
        return self.db.search(where('name') == std_helper.stringify(pkg_name))

    @staticmethod
    def __update_record(pkg):
        """Helper function to update a record."""
        def transform(element):
            element["ver"] = pkg["pkg_ver"]
            element["desc"] = pkg["pkg_desc"]
        return transform
