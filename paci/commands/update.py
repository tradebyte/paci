"""The update command."""

from paci.helpers.pkg_install import PkgInstall
from .base import Base


class Update(Base):
    """Updates a package!"""

    def run(self):
        install_helper = PkgInstall(self.settings, self.options, self.index, self.repo_cache, True)
        pkg_names = self.options["<package>"]

        for pkg_name in pkg_names:
            # print(self.index.get_pkg(pkg_name)) maybe add some restrictions... no new version no update?
            install_helper.install(pkg_name, self.base_pkg_dir)
