"""Helper to deal with the repo cache"""

import os
from tinydb import *


def find_pkg(name, repo_list, cache_path):
    """Find a package in the cached repo index files"""
    for repo in sorted(repo_list)[::-1]:
        file = os.path.join(cache_path, "{}.json".format(repo))
        if os.path.exists(file):
            db = TinyDB(file)
            res = db.search(Query().name == name)
            if res:
                return [[res[0]["name"], res[0]["ver"], res[0]["desc"], repo]]
            else:
                return None
        else:
            print("Error! No cache found! Please use `paci refresh` first!")
            exit(1)


def get_pkg_url(name, repo_list, cache_path):
    """Get the repo url of a package"""
    res = find_pkg(name, repo_list, cache_path)
    if res:
        return repo_list[res[0][3]]
    else:
        return None
