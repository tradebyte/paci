"""The update command."""

from .base import Base


class Update(Base):
    """Updates a package!"""

    def run(self):
        print('NYI!')
        # Update if version is different: db.search(Query().name != pkg_constants['pkg_ver'])
