from . import oceanonly
from . import crunchy

__all__ = [
    'MACHINES',
]

MACHINES = [
    oceanonly,
    crunchy,
]

import os

if 'KW_BUILDBOT_TESTING' in os.environ:
    from . import local
    MACHINES = [local]
