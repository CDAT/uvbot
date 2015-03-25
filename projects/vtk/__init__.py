import projects

__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'vtk'

DEFAULTS = {
    'configure_options:project': {
        'BUILD_EXAMPLES:BOOL': 'ON',
        'BUILD_TESTING:BOOL': 'ON',
        'VTK_DEBUG_LEAKS:BOOL': 'ON',
        'VTK_LEGACY_REMOVE:BOOL': 'ON',
        'VTK_USER_LARGE_DATA:BOOL': 'ON',
    },
}

OPTIONS = {
    'os': {
        'linux': {},
        'windows': {},
        'osx': {},
    },
    'libtype': {
        'shared': {
            'configure_options:project': {
                'BUILD_SHARED_LIBS:BOOL': 'ON',
            },
        },
        'static': {
            'configure_options:project': {
                'BUILD_SHARED_LIBS:BOOL': 'OFF',
            },
        },
    },
    'buildtype': {
        'release': {
            'configure_options:project': {
                'CMAKE_BUILD_TYPE:STRING': 'Release',
            },
        },
        'debug': {
            'configure_options:project': {
                'CMAKE_BUILD_TYPE:STRING': 'Debug',
            },
        },
        'relwithdebinfo': {
            'configure_options:project': {
                'CMAKE_BUILD_TYPE:STRING': 'RelWithDebInfo',
            },
        },
    },
    'category': {
        'expected': {},
        'exotic': {},
        'experimental': {},
        'default' : 'expected',
    },
}
OPTIONORDER = ('os', 'libtype', 'buildtype',)

FEATURES = {
    'python': projects.make_feature_cmake_options({
        'VTK_WRAP_PYTHON:BOOL': ('OFF', 'ON'),
    }),
    'tcl': projects.make_feature_cmake_options({
        'VTK_WRAP_TCL:BOOL': ('OFF', 'ON'),
    }),
    'java': projects.make_feature_cmake_options({
        'VTK_WRAP_JAVA:BOOL': ('OFF', 'ON'),
    }),
    'kits': projects.make_feature_cmake_options({
        'VTK_ENABLE_KITS:BOOL': ('OFF', 'ON'),
    }),
    'mpi': projects.make_feature_cmake_options({
        'VTK_Group_MPI:BOOL': ('OFF', 'ON'),
    }),
    'qt': projects.make_feature_cmake_options({
        'VTK_Group_Qt:STRING': ('OFF', 'ON'),
    }),
    'qt5': projects.make_feature_cmake_options({
        'VTK_QT_VERSION:STRING': ('4', '5'),
    }),
    'opengl2': projects.make_feature_cmake_options({
        'VTK_RENDERING_BACKEND:STRING': ('OpenGL', 'OpenGL2'),
    }),
    'icc': ({}, {}),
    'clang': ({}, {}),
    'tbb': ({}, {}),
    'vs': ({}, {
        'configure_options:feature': {
            'CMAKE_CXX_MP_FLAG:BOOL': 'ON',
        },
    }),
    'asan': ({}, {}),
    'ubsan': ({}, {}),

    '_noexamples': ({}, {
        'configure_options:feature': {
            'BUILD_EXAMPLES:BOOL': 'OFF',
        },
    }),
}
