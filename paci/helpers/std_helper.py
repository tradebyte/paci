"""Helper to deal with common tasks"""


def stringify(obj):
    if type(obj) is list:
        return ''.join(obj)
    else:
        return str(obj)
