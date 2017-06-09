"""The update command."""

from .base import Base
from paci.helpers.pkg_install import PkgInstall


class Update(Base):
    """Updates a package!"""

    def run(self):
        install_helper = PkgInstall(self.settings, self.options, self.index, self.repo_cache)
        pkg_names = self.options["<package>"]
        pkg_files = {
            "GET.json": "",
            "UPDATE.sh": "",
            "INSTALL.sh": "",
            "DESKTOP": "",
            "CONF.tar.gz": "",
        }

        for pkg_name in pkg_names:
            # print(self.index.get_pkg(pkg_name)) maybe add some restrictions... no new version no update?
            install_helper.install(pkg_files, pkg_name, self.base_pkg_dir)

