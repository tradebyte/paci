"""Helper to output stuff"""

from tabulate import tabulate


def print_list(header, entries):
    """Prints out a list"""
    print(tabulate(entries, header, tablefmt="grid"))


def print_table(entries):
    """Prints out a table"""
    print(tabulate(entries, tablefmt="plain"))


def std_input(text, default):
    """Get input or return default if none is given."""
    return input(text.format(default)) or default
