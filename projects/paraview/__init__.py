import projects

__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'paraview'

DEFAULTS = {
    'test_include_labels:project': [
        'PARAVIEW',
    ],
    'configure_options:project': {
        'BUILD_EXAMPLES:BOOL': 'ON',
        'VTK_DEBUG_LEAKS:BOOL': 'ON',
        'VTK_LEGACY_REMOVE:BOOL': 'ON',
        'PARAVIEW_ENABLE_CATALYST:BOOL': 'ON',
        'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
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
            }
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
    },
    'category': {
        'expected': {},
        'exotic': {},
        'experimental': {},
        'default' : 'expected',
    },
}
OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'python': projects.make_feature_cmake_options({
        'PARAVIEW_ENABLE_PYTHON:BOOL': ('OFF', 'ON'),
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
    'gui': projects.make_feature_cmake_options({
        'PARAVIEW_BUILD_QT_GUI:BOOL': ('OFF', 'ON'),
    }),
    'mpi': projects.make_feature_cmake_options({
        'PARAVIEW_USE_MPI:BOOL': ('OFF', 'ON'),
    }),
    'qt5': projects.make_feature_cmake_options({
        'PARAVIEW_QT_VERSION:STRING': ('4', '5'),
    }),
    'unified': projects.make_feature_cmake_options({
        'PARAVIEW_USE_UNIFIED_BINDINGS:BOOL': ('OFF', 'ON'),
    }),
    'opengl2': projects.make_feature_cmake_options({
        'VTK_RENDERING_BACKEND:STRING': ('OpenGL', 'OpenGL2'),
        # TODO - These plugins don't work with OpenGL2 and are
        #        enabled by default
        'PARAVIEW_BUILD_PLUGIN_PointSprite:BOOL': ('TRUE', 'FALSE'),
        'PARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL': ('TRUE', 'FALSE'),
        'PARAVIEW_BUILD_PLUGIN_SciberQuestToolKit:BOOL': ('TRUE', 'FALSE'),
    }),
    'icc': ({}, {
        'slaveenv': {
            'CC': 'icc',
            'CXX': 'icpc',
        }
    }),
    'vs': ({}, {
        'configure_options:feature': {
            'CMAKE_CXX_MP_FLAG:BOOL': 'ON',
        },
    }),
    '32bit': ({}, {}),
}
