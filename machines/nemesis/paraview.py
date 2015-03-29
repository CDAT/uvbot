import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        'SurfaceLIC-ShuttleAll', # seems the streamlines aren't thick enough?
        'NonlinearSubdivisionDisplay', # missing mesh edges?
    ],

    'configure_options:builderconfig': {
        'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Users/kitware/misc/root/qt-4.8.6/bin/qmake.exe',

        'PARAVIEW_DATA_STORE:PATH': 'C:/Users/kitware/dashboards/data/paraview',
    },
}

base_features = (
    'gui',
    'python',
    'mpi',

    '_noexamples',
)
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
    {
        'os': 'windows',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets, defprops,
        dirlen=8)

kitbuildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features + (
            'kits',
        ),
    },
    {
        'os': 'windows',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features + (
            'kits',
        ),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, paraview, kitbuildsets, defprops,
    dirlen=8)
