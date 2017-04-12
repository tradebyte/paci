"""Helper to output stuff"""


def print_list(header, entries):
    """Prints out a list"""

    # Add the header
    entries.insert(0, header)

    # Get the width
    col_width = max(len(word) for entry in entries for word in entry) + 2

    # Print everything
    for entry in entries:
        print("".join(word.ljust(col_width) for word in entry))
