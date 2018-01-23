"""Helper to output stuff"""

from tabulate import tabulate
import os


def print_list(header, entries):
    """Prints out a list"""
    print(tabulate(fix_descriptions(entries), header, tablefmt="presto"))


def print_table(entries):
    """Prints out a table"""
    print(tabulate(cleanup_entries(entries), tablefmt="plain"))


def std_input(text, default):
    """Get input or return default if none is given."""
    return input(text.format(default)) or default


def fix_descriptions(entries):
    """Fixes the description to fit into the terminal"""

    clean_entries = []
    ml = get_max_desc_width(get_longest_list(entries))

    for entry in entries:
        clean_entry = entry
        max_value = max(entry, key=len)
        for idx, val in enumerate(entry):
            if val is max_value:
                clean_entry[idx] = entry[idx][:ml] + (entry[idx][ml:] and ' [..]')
        clean_entries.append(clean_entry)

    return clean_entries


def get_longest_list(entries):
    max_list = ['']*len(entries[0])
    for entry in entries:
        for idx, val in enumerate(entry):
            if len(val) > len(max_list[idx]):
                max_list[idx] = val
    return max_list


def get_max_desc_width(lst):
    _, columns = os.popen('stty size', 'r').read().split()
    length = int(columns)
    max_value = max(lst, key=len)
    for val in lst:
        if val is not max_value:
            length -= len(val)

    return length - 15
