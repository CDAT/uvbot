import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {}
env = {
    'PATH': 'C:/Support/Qt/4.8.0-vs2010-x64/bin;C:/Python27x64;${PATH}',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'OFF',
    'BUILD_TESTING:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_DATA_STORE:PATH': 'C:/Dashboards/CDashHome/ExternalData',
    'VTK_USER_LARGE_DATA:BOOL': 'ON',

    'CMAKE_CXX_MP_FLAG:BOOL': 'ON',
}

buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'mpi',
            'qt',
            'vs',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    env=env
)
