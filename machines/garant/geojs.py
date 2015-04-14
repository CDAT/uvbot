from buildbot import locks

import projects
from projects import geojs
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
    ],

    'configure_options:builderconfig': {
        'TESTING_PORT': '8101',
        'SELENIUM_HOST': 'garant'
    },

    'slaveenv': {
    },
    'webport': '8101'
}

base_features = (
)

buildsets = [
    {
        'os': 'linux',
        'features': ('selenium', 'chrome'),
        'buildtype': 'release'
    },
]

locks = [
    locks.SlaveLock("web_server", maxCount=1).access('exclusive')
]

BUILDERS = projects.make_builders(slave, geojs, buildsets, defprops, locks=locks)
