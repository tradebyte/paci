from .install import Install
from .configure import Configure
from .update import Update
from .list import List
from .generate import Generate

COMMANDS = {
    'install': Install,
    'configure': Configure,
    'update': Update,
    'list': List,
    'generate': Generate,
}
