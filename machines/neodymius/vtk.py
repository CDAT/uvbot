import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData/vtk',
    },

    'slaveenv': {
        'DISPLAY': ':0',
    },
}

allprops = projects.merge_config(defprops, {
    'compiler': 'icc-14.0.0',

    'configure_options:builderconfig': {
        'VTK_BUILD_ALL_MODULES:BOOL': 'ON',
        'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',
    },
})

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'python',
            'java',

            'icc',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets, allprops)

gccbuildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'python',
            'java',
        ),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, vtk, gccbuildsets, defprops)
