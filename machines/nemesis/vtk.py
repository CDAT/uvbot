import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'vcvarsall': 'C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat',
    'vcvarsargument': 'x64',
}

defconfig = {
    # Examples end up with commands that are way too long.
    #'BUILD_EXAMPLES:BOOL': 'ON',
    'BUILD_TESTING:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_LEGACY_REMOVE:BOOL': 'ON',

    'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Users/kitware/misc/root/qt-4.8.6/bin/qmake.exe',

    'VTK_DATA_STORE:PATH': 'C:/Users/kitware/dashboards/data/vtk',
}

base_features = (
    'opengl2',
    'python',
    'mpi',
)
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets,
    defprops=defprops,
    defconfig=defconfig
)
