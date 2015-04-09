from . import curius

__all__ = [
    'MACHINES',
]

MACHINES = [
    curius,
]

import os

if 'KW_BUILDBOT_TESTING' in os.environ:
    from . import local
    MACHINES = [local]
