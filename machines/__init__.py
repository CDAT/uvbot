from . import amber8
from . import bigmac
from . import blight
from . import dashlin1
from . import debian4dash
from . import debian5dash
from . import debian6dash
from . import debian7dash
from . import endor
from . import hythloth
from . import kamino
from . import megas
from . import miranda
from . import nemesis
from . import neodymius
from . import renar
from . import talosiv
from . import tarvalon
from . import trey

__all__ = [
    'MACHINES',
]

MACHINES = [
    amber8,
    bigmac,
    blight,
    dashlin1,
    debian4dash,
    #debian5dash,
    #debian6dash,
    #debian7dash,
    endor,
    hythloth,
    kamino,
    megas,
    miranda,
    nemesis,
    neodymius,
    renar,
    talosiv,
    tarvalon,
    trey,
]

import os

if 'KW_BUILDBOT_TESTING' in os.environ:
    from . import local
    MACHINES = [local]
