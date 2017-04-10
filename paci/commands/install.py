# -*- coding: utf-8 -*-
"""The install command."""

import tempfile
import os
import shutil
from .base import Base
from paci.helpers import download_helper, file_helper, cmd_helper


class Install(Base):
    """Install!"""

    def run(self):
        pkg_name = self.options['<package>']
        pkg_url = self.settings["paci"]["registry"]["main"] + "/" + pkg_name  # TODO: handle fallback repo

        pkg_files = {
            'GET.json': '',
            'INSTALL.sh': '',
            'DESKTOP': '',
            'CONF.tar.gz': '',
        }

        # Create temporary package directory
        os.makedirs(self.settings["paci"]["temp"], exist_ok=True)
        pkg_temp_dir = tempfile.mkdtemp(dir=self.settings["paci"]["temp"], prefix=pkg_name + '_')

        # Download RECIPE.yml
        pkg_recipe = download_helper.download(pkg_url + "/RECIPE.yml", pkg_temp_dir, hidden=True)
        pkg_conf = file_helper.get_pkg_conf(pkg_recipe)

        # Create package directory
        pkg_dir = self.settings["paci"]["base"] + "/apps/" + pkg_name + "_" + pkg_conf['version']
        os.makedirs(pkg_dir, exist_ok=True)

        # Create package constants (e.g. used for the templates)
        pkg_vars = {
            'pkg_src': pkg_temp_dir,
            'pkg_dir': pkg_dir,
            'pkg_ver': pkg_conf['version'],
            'pkg_desc': pkg_conf['summary'],
            'pkg_name': pkg_conf['name']
        }

        print("Package: " + pkg_vars['pkg_name'] + " (v" + pkg_vars['pkg_ver'] + ")")
        print("Package working directory: " + pkg_temp_dir + "\n")
        print("Downloading files...")

        # Download all meta files
        for (file, path) in pkg_files.items():
            pkg_files[file] = download_helper.download(pkg_url + "/" + file, pkg_temp_dir)

        if 'sources' in pkg_conf:
            pkg_files['SOURCES.tar.gz'] = download_helper.download(
                pkg_url + "/" + pkg_conf['sources'],
                pkg_vars['pkg_src'],
                pkg_conf['sha512sum']
            )

        if pkg_files['SOURCES.tar.gz']:
            file_helper.extract_tar_gz(pkg_vars['pkg_src'] + '/SOURCES', pkg_files['SOURCES.tar.gz'])

        if pkg_files['GET.json']:
            download_helper.download_get_files(pkg_files['GET.json'], pkg_vars['pkg_src'], pkg_vars)

        if pkg_files['INSTALL.sh']:
            print("\nInstalling package...")
            cmd_helper.set_script_variables(pkg_vars)
            cmd_helper.execute_shell_script(pkg_files['INSTALL.sh'], pkg_vars['pkg_src'])

        if pkg_files['DESKTOP']:
            file_helper.create_desktop_file(pkg_vars, pkg_files['DESKTOP'])

        if pkg_files['CONF.tar.gz'] and not self.options['--no-config']:
            conf_dir = pkg_vars['pkg_src'] + '/CONF'
            file_helper.extract_tar_gz(conf_dir, pkg_files['CONF.tar.gz'])
            cmd_helper.rsync(pkg_vars['pkg_src'], conf_dir, os.environ.get('HOME'))

        # Cleanup if successful
        if not self.options['--no-cleanup']:
            shutil.rmtree(pkg_temp_dir)

        # Add package to the installed packages list
        self.index.add(pkg_vars)

        print("\n"
              + pkg_vars['pkg_name']
              + " (v" + pkg_vars['pkg_ver'] + ")"
              + " successfully installed!"
              )
