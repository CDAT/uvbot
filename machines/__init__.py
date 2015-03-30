from . import amber8
from . import blight
from . import dashlin1
from . import debian4dash
from . import debian5dash
from . import debian6dash
from . import debian7dash
from . import kamino
from . import megas
from . import nemesis
from . import neodymius
from . import tarvalon
from . import trey
from . import miranda

__all__ = [
    'MACHINES',
]

MACHINES = [
    amber8,
    blight,
    dashlin1,
    debian4dash,
    #debian5dash,
    #debian6dash,
    #debian7dash,
    kamino,
    megas,
    nemesis,
    neodymius,
    tarvalon,
    trey,
    miranda
]

import os

if 'KW_BUILDBOT_TESTING' in os.environ:
    from . import local
    MACHINES = [local]
