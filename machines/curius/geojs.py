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

#    'referencedir': '/home/kitware/dashboards/buildbot-share/paraview',

    'slaveenv': {
        'DISPLAY': ':0',
        'PATH': '${PATH}',
    },
}

base_features = (
#    'gui',
#    'python',
#    'kits',
#    'mpi',
)
buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
#    {
#        'os': 'linux',
#        'libtype': 'static',
#        'buildtype': 'release',
#        'features': base_features,
#    },
]

BUILDERS = projects.make_builders(slave, geojs, buildsets, defprops)
