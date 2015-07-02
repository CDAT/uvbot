import projects
from projects import uvcdat
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
    ],

    'slaveenv': {
        'DISPLAY': ':0'
    },
    'webport': '8101'
}

base_features = (
)

buildsets = [
    {
        'os': 'linux',
        'buildtype': 'release',
        'gui': 'OFF'
    },
]

BUILDERS = projects.make_builders(slave, uvcdat, buildsets, defprops)
