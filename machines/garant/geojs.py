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
        'SELENIUM_PORT': '8101'
    },

    'slaveenv': {
    },
}

base_features = (
)

buildsets = [
    {
        'os': 'linux',
        'features': ('selenium', 'chrome')
    },
]

BUILDERS = projects.make_builders(slave, geojs, buildsets, defprops)
