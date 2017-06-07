"""Helper to output stuff"""

from tabulate import *


def print_list(header, entries):
    """Prints out a list"""
    print(tabulate(entries, header, tablefmt="grid"))


def std_input(text, default):
    return input(text.format(default)) or default
