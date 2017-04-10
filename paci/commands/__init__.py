from .install import Install
from .configure import Configure
from .update import Update
from .list import List

COMMANDS = {
    'install': Install,
    'configure': Configure,
    'update': Update,
    'list': List,
}
