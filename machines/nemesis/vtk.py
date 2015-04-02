import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Users/kitware/misc/root/qt-4.8.6/bin/qmake.exe',

        'VTK_DATA_STORE:PATH': 'C:/Users/kitware/dashboards/data/vtk',
    },
}

base_features = (
    'opengl2',
    'python',
    'mpi',

    '_noexamples',
    '_noparallel',
)
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)
