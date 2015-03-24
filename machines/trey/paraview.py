import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'generator': 'Ninja',

    'test_include_labels:builderconfig': [
        'CATALYST',
        'PARAVIEWWEB',
    ],
    'test_excludes:builderconfig': [
        'ProbePicking', # flaky
        'TestPythonView', # bad on OS X
        'HistogramSelection', # viewport too small (image corruption)
        'SelectionLabels', # http://www.paraview.org/Bug/view.php?id=15294
    ],

    'configure_options:builderconfig': {
        'PARAVIEW_DATA_STORE:PATH': '/Users/kitware/dashboards/data',

        'VTK_USE_SYSTEM_EXPAT:BOOL': 'ON',
        'VTK_USE_SYSTEM_JPEG:BOOL': 'ON',
        'VTK_USE_SYSTEM_LIBXML2:BOOL': 'ON',
        'VTK_USE_SYSTEM_PNG:BOOL': 'ON',
        'VTK_USE_SYSTEM_TIFF:BOOL': 'ON',
        'VTK_USE_SYSTEM_ZLIB:BOOL': 'ON',
    },
}

base_features = (
    'gui',
    'kits',
    'python',
)
buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
    {
        'os': 'osx',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets, defprops)
