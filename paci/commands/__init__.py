"""Initialize all commands which are usable in paci."""

from .install import Install
from .configure import Configure
from .update import Update
from .list import List
from .generate import Generate
from .remove import Remove
from .refresh import Refresh
from .search import Search

COMMANDS = {
    "install": Install,
    "configure": Configure,
    "update": Update,
    "list": List,
    "generate": Generate,
    "remove": Remove,
    "refresh": Refresh,
    "search": Search,
}
