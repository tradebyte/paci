"""The generate command."""

import os
from paci.helpers import file_helper
from paci.helpers.pkg_index import PkgIndex
from .base import Base


class Generate(Base):
    """Generate index files!"""

    def run(self):
        if self.options["pkg-index"]:
            print("Regenerating the index file for all installed packages...")

            file_helper.safe_delete(self.index_file)
            pkg_db = PkgIndex(self.index_file)

            pkg_count = self.generate_index(pkg_db, self.base_pkg_dir)
            print("{} packages written to: {}".format(pkg_count, self.index_file))

        if self.options["repo-index"]:
            repo_path = self.options["<path>"]
            print("Generating the index file for all packages inside a repository...")

            if os.path.isabs(repo_path):
                repo_file = os.path.join(repo_path, "index.json")

                file_helper.safe_delete(repo_file)
                repo_db = PkgIndex(repo_file)

                pkg_count = self.generate_index(repo_db, repo_path)
                print("{} packages written to: {}".format(pkg_count, repo_file))
            else:
                print("Error! Please provide an absolute path to your repository!")
                exit(1)

    @staticmethod
    def generate_index(index_db, path):
        """Generates an index file from the folders in the path."""
        pkg_count = 0

        for root, dirs, files in os.walk(path):
            files = [f for f in files if not f[0] == "."]
            dirs[:] = [d for d in dirs if not d[0] == "."]

            if "RECIPE.yml" in files:
                pkg_conf = file_helper.get_pkg_conf(os.path.join(root, "RECIPE.yml"))
                index_db.add({
                    "pkg_ver": pkg_conf["version"],
                    "pkg_desc": pkg_conf["summary"],
                    "pkg_name": pkg_conf["name"]
                })
                pkg_count += 1

        return pkg_count
