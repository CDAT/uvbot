from . import oceanonly

__all__ = [
    'MACHINES',
]

MACHINES = [
    oceanonly,
]

import os

if 'KW_BUILDBOT_TESTING' in os.environ:
    from . import local
    MACHINES = [local]
