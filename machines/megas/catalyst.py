import projects
from projects import catalyst
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'referencedir': '/home/kitware/dashboards/buildbot-share/paraview',

    'slaveenv': {
        'DISPLAY': ':1',
        'PATH': '/usr/lib64/mpich/bin:${PATH}',
    },
    'test_excludes:builderconfig': [
        # This is legitimate failure that needs to be addressed.
        'import-essentials',
    ],
}

buildsets = [
    {
        'os': 'linux',
        'buildtype': 'release',
        'features': ('catalyst',),
    },
]

BUILDERS = projects.make_builders(slave, catalyst, buildsets, defprops)
