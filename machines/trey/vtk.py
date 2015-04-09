import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/Users/kitware/dashboards/data',
    },
}

base_features = (
    'python',
    'qt',
)
buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features + (
            '_strict',
        ),
    },
]

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)
