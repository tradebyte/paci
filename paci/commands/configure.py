"""The configure command lets you define a settings.yml for paci."""

from .base import Base


class Configure(Base):
    """Creates a settings.yml for paci interactive with the user."""

    def run(self):
        print('Lets configure a new settings.yml for paci!')
        newarg = input('basedir (defaults to $HOME/.paci/: ')
        print(newarg)

