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
    },

    'slaveenv': {
        'DISPLAY': ':0',
        'PATH': '${PATH}',
    },
}

base_features = (
)

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave, geojs, buildsets, defprops)
