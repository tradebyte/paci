"""Helper class to deal with the index.json"""

from tinydb import *


class PkgIndex(object):
    """Helper for managing the packages index.json file"""

    def __init__(self, base):
        """Initializes the setting path and the default setting values."""
        self.db = TinyDB(base + "/pkgs.json")

    def add(self, pkg):
        query = Query()
        if not self.db.search(query.name == pkg['pkg_name']):
            # Create
            self.db.insert({'name': pkg['pkg_name'],
                            'ver': pkg['pkg_ver'],
                            'desc': pkg['pkg_desc']
                            })
        elif self.db.search((query.name == pkg['pkg_name']) & (query.ver != pkg['pkg_ver'])):
            # Update
            self.db.update(self.__update_record(pkg), query.name == pkg['pkg_name'])

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
