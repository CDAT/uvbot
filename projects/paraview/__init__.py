import projects
from projects.common import features
from projects.common import options

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

    'cdash_url': 'https://open.cdash.org',
    'cdash_project': 'ParaView',
}

OPTIONS = {
    'os': options.os,
    'libtype': options.libtypes,
    'buildtype': options.buildtypes,
    'category': options.categories,
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
    }, extra_with={
        'test_excludes:feature': [
            # Enough problems that these are just noise right now.
            '^pvcs\.',
            '^pvcrs\.',
        ],
    }),
    'icc': features.icc,
    'vs': features.vs,
    'clang': features.clang,
    '32bit': ({}, {}),

    '_nocollab': ({}, {
        'configure_options:feature': {
            'PARAVIEW_COLLABORATION_TESTING:BOOL': 'OFF',
        },
    }),

    '_noexamples': ({}, {
        'configure_options:feature': {
            'BUILD_EXAMPLES:BOOL': 'OFF',
        },
    }),
    # Don't use with +gui for now
    'osmesa': ({}, {
        'configure_options:feature': {
            'VTK_OPENGL_HAS_OSMESA:BOOL': 'ON',
            'VTK_USE_OFFSCREEN:BOOL': 'ON',
            'VTK_USE_X:BOOL': 'OFF',
            'OPENGL_gl_LIBRARY:FILEPATH': '',
            'OPENGL_glu_LIBRARY:FILEPATH': '',
        },
    }),

    '_strict': features.strict,
    '_parallel': features.parallel,
}
