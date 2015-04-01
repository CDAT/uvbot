import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'clang-apple-6.0',

    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/Users/kitware/VTKData',
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
            'gui',
            'opengl2',
        ),
    }
]

BUILDERS = projects.make_builders(slave, paraview, buildsets, defprops)
