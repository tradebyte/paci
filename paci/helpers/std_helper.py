"""Helper to deal with common tasks"""


def stringify(obj):
    """Helper method which converts any given object into a string."""

    if isinstance(obj, list):
        return ''.join(obj)
    else:
        return str(obj)
