# -*- coding: utf-8 -*-
"""
paci

Usage:
  paci install [--no-config] [--no-cleanup] [--reuse] [--overwrite] [--debug] <package>...
  paci update [--no-config] [--no-cleanup] [--reuse] [--overwrite] [--debug] <package>...
  paci search <package>
  paci refresh
  paci list [--installed]
  paci remove
  paci configure [--no-choice] [--silent] [--main-registry=<url>] [--fallback-registry=<url>]
  paci generate (repo-index <path> | pkg-index)
  paci --help
  paci --version

Options:
  -h, --help                         Show this screen.
  -v, --version                      Show version.
  -n, --no-config                    Omits the config.
  -c, --no-cleanup                   Don't cleanup the mess.
  -o, --overwrite                    Overwrite the config.
  -d, --debug                        Print debugging messages.
  -i, --installed                    List all installed packages.
  -r, --reuse                        Reuse the downloaded files.
                                     (only possible with --no-cleanup)
  --no-choice                        Omit the questions and use the defaults.
  --silent                           Don't print anything.
  --main-registry=<url>              Set the <url> as default for the main registry.
  --fallback-registry=<url>          Set the <url> as default for the fallback registry.

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
