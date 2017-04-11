# -*- coding: utf-8 -*-
"""
paci

Usage:
  paci install [--no-config] [--no-cleanup] <package>
  paci update [--no-config] <package>
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

Examples:
  paci install phpstorm

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/tradebyte/paci
"""

import better_exceptions
from docopt import docopt
from . import __version__ as version
from paci.commands import COMMANDS


def main():
    """Main CLI entry point."""
    import paci.commands
    options = docopt(__doc__, version=version)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(paci.commands, k) and v:
            command = COMMANDS[k](options)
            command.run()

