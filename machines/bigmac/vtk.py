import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'clang-apple-6.0',

    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/Users/kitware/VTKData',
        'CTEST_TEST_TIMEOUT': '120',
    },

}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'debug',
        'category': 'experimental',
        'features': (
            'clang',
            'python',
            '_parallel',
        ),
    },
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'debug',
        'category': 'experimental',
        'features': (
            'clang',
            'python',
            'opengl2',
        ),
    }
]

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)
