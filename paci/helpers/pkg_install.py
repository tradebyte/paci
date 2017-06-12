"""Helper to deal with the installation of a package"""

import tempfile
import os
import shutil
from paci.helpers import download_helper, file_helper, cmd_helper, cache_helper


class PkgInstall(object):
    """Helper for managing the installation of packages"""

    def __init__(self, settings, options, index, repo_cache, update=False):
        """Initializes the default settings."""
        self.settings = settings
        self.options = options
        self.index = index
        self.repo_cache = repo_cache
        self.update = update

    def install(self, pkg_name, base_pkg_dir):
        """Main function to walk through the installation."""
        repo_url = cache_helper.get_pkg_url(pkg_name, self.settings["paci"]["registry"], self.repo_cache)

        pkg_files = {
            "GET.json": "",
            "INSTALL.sh": "",
            "DESKTOP": "",
            "CONF.tar.gz": "",
        }

        if self.update:
            pkg_files.update({"UPDATE.sh": ""})

        if repo_url:
            pkg_url = os.path.join(repo_url, pkg_name)

            ##########################################
            # Step 1: Setup temp folder and RECIPE.yml
            ##########################################

            if self.options["--reuse"]:
                temp_dir = self.settings["paci"]["temp"]

                # Find the old temporary package directory
                sub_dirs = [name for name in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, name))]
                matching_dirs = filter(lambda k: pkg_name in k, sub_dirs)
                latest_dir = max([os.path.join(temp_dir, name) for name in matching_dirs], key=os.path.getmtime)

                pkg_temp_dir = latest_dir
                pkg_recipe = os.path.join(pkg_temp_dir, "RECIPE.yml")

            else:
                # Create temporary package directory
                pkg_temp_dir = tempfile.mkdtemp(dir=self.settings["paci"]["temp"], prefix=pkg_name + "_")

                # Download RECIPE.yml
                # pylint: disable=redefined-variable-type
                # no error
                pkg_recipe = download_helper.download(os.path.join(pkg_url, "RECIPE.yml"), pkg_temp_dir, hidden=True)

            ################################
            # Step 2: Setup vars and folders
            ################################

            # Get the package configuration
            pkg_conf = file_helper.get_pkg_conf(pkg_recipe)

            # Create package directory
            pkg_dir = os.path.join(base_pkg_dir, "{}_{}".format(pkg_name, pkg_conf["version"]))
            os.makedirs(pkg_dir, exist_ok=True)

            # Create package constants (e.g. used for the templates)
            pkg_vars = {
                "pkg_src": pkg_temp_dir,
                "pkg_dir": pkg_dir,
                "pkg_ver": pkg_conf["version"],
                "pkg_desc": pkg_conf["summary"],
                "pkg_name": pkg_conf["name"]
            }

            print("Package: {} (v{})".format(pkg_vars["pkg_name"], pkg_vars["pkg_ver"]))
            print("Package working directory: {}\n".format(pkg_temp_dir))

            ###################################
            # Step 3: Download all needed files
            ###################################
            self.__download(pkg_conf, pkg_files, pkg_temp_dir, pkg_url, pkg_vars)

            ############################
            # Step 4: Start Installation
            ############################
            self.__run_install(pkg_files, pkg_vars)

            ######################
            # Step 5: Post Install
            ######################
            self.__post_install(pkg_dir, pkg_recipe, pkg_temp_dir, pkg_vars)
        else:
            print("Error! Package not found!")
            exit(1)

    def __download(self, pkg_conf, pkg_files, pkg_temp_dir, pkg_url, pkg_vars):
        """Download all needed files."""

        if self.options["--reuse"]:
            print("Reusing files...")
            # Provide path to all files needed
            for (file, _) in pkg_files.items():
                pkg_files[file] = os.path.join(pkg_temp_dir, file)
        else:
            print("Downloading files...")

            # Download all meta files
            for (file, _) in pkg_files.items():
                pkg_files[file] = download_helper.download(os.path.join(pkg_url, file), pkg_temp_dir)

            if "sources" in pkg_conf:
                pkg_files["SOURCES.tar.gz"] = download_helper.download(
                    os.path.join(pkg_url, pkg_conf["sources"]),
                    pkg_vars["pkg_src"],
                    pkg_conf["sha512sum"]
                )

            if "SOURCES.tar.gz" in pkg_files:
                file_helper.extract_tar_gz(os.path.join(pkg_vars["pkg_src"], "SOURCES"),
                                           pkg_files["SOURCES.tar.gz"])

            if pkg_files["GET.json"]:
                download_helper.download_get_files(pkg_files["GET.json"], pkg_vars["pkg_src"], pkg_vars)

    def __run_install(self, pkg_files, pkg_vars):
        """Execute the install/update script and move all files to the right place."""

        skip_install_sh = False

        if "UPDATE.sh" in pkg_files:
            if pkg_files["UPDATE.sh"]:
                print("\nUpdating package...")
                cmd_helper.set_script_variables(pkg_vars)
                cmd_helper.execute_shell_script(pkg_files["UPDATE.sh"], pkg_vars["pkg_src"])
                skip_install_sh = True

        if "INSTALL.sh" in pkg_files:
            if pkg_files["INSTALL.sh"] and not skip_install_sh:
                print("\nInstalling package...")
                cmd_helper.set_script_variables(pkg_vars)
                cmd_helper.execute_shell_script(pkg_files["INSTALL.sh"], pkg_vars["pkg_src"])

        if "DESKTOP" in pkg_files:
            if pkg_files["DESKTOP"]:
                file_helper.create_desktop_file(pkg_vars, pkg_files["DESKTOP"])

        if "CONF.tar.gz" in pkg_files and not self.options["--no-config"]:
            if pkg_files["CONF.tar.gz"]:
                conf_dir = os.path.join(pkg_vars["pkg_src"], "CONF")
                file_helper.extract_tar_gz(conf_dir, pkg_files["CONF.tar.gz"])
                cmd_helper.rsync(
                    pkg_vars["pkg_src"],
                    conf_dir, os.environ.get("HOME"),
                    False if self.options["--overwrite"] else True
                )

    def __post_install(self, pkg_dir, pkg_recipe, pkg_temp_dir, pkg_vars):
        """Handles post install tasks. Such as removing junk and adding the package to the index."""

        # Add RECIPE.yml to the pkg
        file_helper.safe_copy(pkg_recipe, pkg_dir)

        # Cleanup if successful
        if not self.options["--no-cleanup"]:
            shutil.rmtree(pkg_temp_dir)

        # Add package to the installed packages list
        self.index.add(pkg_vars)
        print("\n{} (v{}) successfully installed!\n".format(pkg_vars["pkg_name"], pkg_vars["pkg_ver"]))
