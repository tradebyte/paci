"""The install command."""


from json import dumps

from .base import Base


class Install(Base):
    """Install!"""

    def run(self):
        print('Hello, world!')
        args = self.options
        # print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        if args['--no-config']:
            print("no-config!")

        print("Package: " + args['<package>'])
