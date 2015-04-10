from projects.common import features
from projects.common import options

__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'geojs'

DEFAULTS = {
    'configure_options:project': {
        'BUILD_EXAMPLES:BOOL': 'ON',
        'BUILD_TESTING:BOOL': 'ON',
    },
    #'supports_parallel_testing:project' : True,

    'cdash_url': 'https://my.cdash.org',
    'cdash_project': 'geojs',
}

OPTIONS = {
    'os': options.os,
    'libtype': options.libtypes,
    'buildtype': options.buildtypes,
    'category': options.categories,
}
OPTIONORDER = ('os', 'libtype', 'buildtype',)

FEATURES = {
#    'python': projects.make_feature_cmake_options({
#        'VTK_WRAP_PYTHON:BOOL': ('OFF', 'ON'),
#    }),
#    'tcl': projects.make_feature_cmake_options({
#        'VTK_WRAP_TCL:BOOL': ('OFF', 'ON'),
#    }),
#    'java': projects.make_feature_cmake_options({
#        'VTK_WRAP_JAVA:BOOL': ('OFF', 'ON'),
#    }),
#    'kits': projects.make_feature_cmake_options({
#        'VTK_ENABLE_KITS:BOOL': ('OFF', 'ON'),
#    }),
#    'mpi': projects.make_feature_cmake_options({
#        'VTK_Group_MPI:BOOL': ('OFF', 'ON'),
#    }),
#    'qt': projects.make_feature_cmake_options({
#        'VTK_Group_Qt:STRING': ('OFF', 'ON'),
#    }),
#    'qt5': projects.make_feature_cmake_options({
#        'VTK_QT_VERSION:STRING': ('4', '5'),
#    }),
#    'opengl2': projects.make_feature_cmake_options({
#        'VTK_RENDERING_BACKEND:STRING': ('OpenGL', 'OpenGL2'),
#    }),
#    'icc': features.icc,
#    'clang': features.clang,
#    'tbb': ({}, {}),
#    'vs': features.vs,
#    'asan': ({}, {}),
#    'ubsan': ({}, {}),

    '_noexamples': ({}, {
        'configure_options:feature': {
            'BUILD_EXAMPLES:BOOL': 'OFF',
        },
    }),

    '_strict': features.strict,
    '_parallel': features.parallel,
}
