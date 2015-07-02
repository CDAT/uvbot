# from . import garant
# from . import test_laptop

__all__ = [
    'MACHINES',
]

MACHINES = [
#    garant,
#    test_laptop,
]

import os

if 'KW_BUILDBOT_TESTING' in os.environ:
    from . import local
    MACHINES = [local]
