# -*- coding: utf-8 -*-
"""
paci

Usage:
  paci install [--no-config] [--no-cleanup] <package>
  paci update [--no-config] <package>
  paci list
  paci remove 
  paci configure
  paci --help
  paci --version

Options:
  -h, --help                         Show this screen.
  -v, --version                      Show version.
  -n, --no-config                    Omits the config.
  -c, --no-cleanup                   Don't cleanup the mess.

Examples:
  paci install --no-config

Help:
  For help using this tool, please open an issue on the Github repository:
  ~~TODO~~
"""

import better_exceptions
from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as version


def main():
    """Main CLI entry point."""
    import paci.commands
    options = docopt(__doc__, version=version)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(paci.commands, k) and v:
            module = getattr(paci.commands, k)
            paci.commands = getmembers(module, isclass)
            command = [command[1] for command in paci.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
