"""Helper class to deal with the index.json"""

from tinydb import *


class PkgIndex(object):
    """Helper for managing the packages index.json file"""

    def __init__(self, path):
        """Initializes the setting path and the default setting values."""
        self.db = TinyDB(path)

    def add(self, pkg, db=None):
        query = Query()

        if not db:
            db = self.db

        # Create
        if not db.search(query.name == pkg['pkg_name']):
            db.insert({'name': pkg['pkg_name'],
                       'ver': pkg['pkg_ver'],
                       'desc': pkg['pkg_desc']
                       })
        # Update
        elif db.search((query.name == pkg['pkg_name']) & (query.ver != pkg['pkg_ver'])):
            db.update(self.__update_record(pkg), query.name == pkg['pkg_name'])

    def get_installed(self):
        pkgs = [["Name", "Version", "Description"]]
        for pkg in self.db.all():
            pkgs.append([pkg['name'], pkg['ver'], pkg['desc']])
        return pkgs

    @staticmethod
    def __update_record(pkg):
        def transform(element):
            element['ver'] = pkg['pkg_ver']
            element['desc'] = pkg['pkg_desc']
        return transform
