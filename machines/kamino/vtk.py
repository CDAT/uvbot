import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # Old GPU drivers.
        'vtkRenderingVolumePython-volTM2DRotateClip',
    ],
}
env = {
    'DYLD_LIBRARY_PATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++:${DYLD_LIBRARY_PATH}',
    'PATH': '/Users/kitware/Dashboards/Support/openmpi/bin:${PATH}',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'BUILD_TESTING:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_DATA_STORE:PATH': '/Users/kitware/Dashboards/ExternalData',
    'VTK_USER_LARGE_DATA:BOOL': 'ON',

    'Module_vtkIOXdmf2:BOOL': 'ON',
    'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',

    'MPIEXEC:FILEPATH': '/Users/kitware/Dashboards/Support/openmpi/bin/orterun',
    'QT_QMAKE_EXECUTABLE:PATH': '/Users/kitware/Dashboards/Support/Qt-4.8.0/bin/qmake',
}

buildsets = [
    {
        'os': 'osx',
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
