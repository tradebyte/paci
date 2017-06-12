"""Helper to deal with the repo cache"""

import os
from tinydb import TinyDB, Query
from fuzzywuzzy import fuzz
from paci.helpers import std_helper


def find_pkg(name, repo_list, cache_path):
    """Find a package in the cached repo index files"""
    found = []
    for repo in sorted(repo_list)[::-1]:
        file = os.path.join(cache_path, "{}.json".format(repo))
        if os.path.exists(file):
            cache_db = TinyDB(file)
            res = cache_db.search(Query().name.test(fuzzy_contains, std_helper.stringify(name)))
            if res:
                for entry in res:
                    if entry not in found:
                        found.append([entry["name"], entry["ver"], entry["desc"], repo])
        else:
            print("Error! No cache found! Please use `paci refresh` first!")
            exit(1)
    if found:
        return found
    else:
        return None


def get_pkg_url(name, repo_list, cache_path):
    """Get the repo url of a package"""
    res = find_pkg(name, repo_list, cache_path)
    if res:
        return repo_list[res[0][3]]
    else:
        return None


def fuzzy_contains(val, name):
    """Fuzzy matches a string"""
    return fuzz.ratio(name, val) >= 50
