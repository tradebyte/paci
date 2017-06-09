# -*- coding: utf-8 -*-
"""The install command."""

from .base import Base
from paci.helpers.pkg_install import PkgInstall


class Install(Base):
    """Install!"""

    def run(self):
        install_helper = PkgInstall(self.settings, self.options, self.index, self.repo_cache)
        pkg_names = self.options["<package>"]
        pkg_files = {
            "GET.json": "",
            "INSTALL.sh": "",
            "DESKTOP": "",
            "CONF.tar.gz": "",
        }

        for pkg_name in pkg_names:
            install_helper.install(pkg_files, pkg_name, self.base_pkg_dir)
