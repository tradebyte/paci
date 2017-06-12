# -*- coding: utf-8 -*-
"""The install command."""

from paci.helpers.pkg_install import PkgInstall
from .base import Base


class Install(Base):
    """Install!"""

    def run(self):
        install_helper = PkgInstall(self.settings, self.options, self.index, self.repo_cache)
        pkg_names = self.options["<package>"]

        for pkg_name in pkg_names:
            install_helper.install(pkg_name, self.base_pkg_dir)
