"""The generate command."""

import os
from .base import Base
from paci.helpers import file_helper
from paci.helpers.pkg_index import PkgIndex


class Generate(Base):
    """Generate index files!"""

    def run(self):
        if self.options["pkg-index"]:
            print("Regenerating the index file for all installed packages...\n")

        if self.options["repo-index"]:
            repo_path = self.options["<path>"]
            print("Generating the index file for all packages inside a repository...\n")

            if os.path.isabs(repo_path):
                repo_file = os.path.join(repo_path, "index.json")

                # Fresh new start
                file_helper.safe_delete(repo_file)
                repo_db = PkgIndex(repo_file)

                for root, dirs, files in os.walk(repo_path):
                    files = [f for f in files if not f[0] == "."]
                    dirs[:] = [d for d in dirs if not d[0] == "."]

                    if "RECIPE.yml" in files:
                        pkg_conf = file_helper.get_pkg_conf(root + "/RECIPE.yml")
                        repo_db.add({
                            "pkg_ver": pkg_conf["version"],
                            "pkg_desc": pkg_conf["summary"],
                            "pkg_name": pkg_conf["name"]
                        })

                print("Index file successfully written to: {}".format(repo_file))
            else:
                print("Error! Please provide an absolute path to your repository!")
                exit(1)
