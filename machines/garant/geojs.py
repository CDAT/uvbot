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

   'selenium': '8101'
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

BUILDERS = projects.make_builders(slave, geojs, buildsets, defprops)
