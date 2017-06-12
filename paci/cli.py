# -*- coding: utf-8 -*-
"""
paci

Usage:
  paci install [--no-config] [--no-cleanup] [--reuse] [--overwrite] <package>...
  paci update [--no-config] [--no-cleanup] [--reuse] [--overwrite] <package>...
  paci search <package>
  paci refresh
  paci list
  paci remove
  paci configure
  paci generate (repo-index <path> | pkg-index)
  paci --help
  paci --version

Options:
  -h, --help                         Show this screen.
  -v, --version                      Show version.
  -n, --no-config                    Omits the config.
  -c, --no-cleanup                   Don't cleanup the mess.
  -o, --overwrite                    Overwrite the config.
  -r, --reuse                        Reuse the downloaded files.
                                     (only possible with --no-cleanup)

Examples:
  paci install phpstorm

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/tradebyte/paci
"""

from docopt import docopt
from paci.commands import COMMANDS
from . import __version__ as version


def main():
    """Main CLI entry point."""
    import paci.commands
    options = docopt(__doc__, version=version)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (key, val) in options.items():
        if hasattr(paci.commands, key) and val:
            command = COMMANDS[key](options)
            command.run()
