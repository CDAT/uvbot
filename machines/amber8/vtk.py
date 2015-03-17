import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # TODO: Most of these are probably Mesa problems.
        'TestPolygonSelection',
    ],
}
env = {
    'DISPLAY': ':0.0',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'BUILD_TESTING:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData',
    'VTK_USER_LARGE_DATA:BOOL': 'ON',

    'Module_vtkIOXdmf2:BOOL': 'ON',
    'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'mpi',
            'python',
            'qt',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    env=env
)
