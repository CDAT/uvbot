from . import garant

__all__ = [
    'MACHINES',
]

MACHINES = [
    garant,
]

import os

if 'KW_BUILDBOT_TESTING' in os.environ:
    from . import local
    MACHINES = [local]
