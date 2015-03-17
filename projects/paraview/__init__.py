__all__ = [
    'NAME',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'paraview'

OPTIONS = {
    'os': {
        'linux': {},
        'windows': {},
        'osx': {},
    },
    'libtype': {
        'shared': {
            'BUILD_SHARED_LIBS:BOOL': 'ON',
        },
        'static': {
            'BUILD_SHARED_LIBS:BOOL': 'OFF',
        },
    },
    'buildtype': {
        'release': {
            'CMAKE_BUILD_TYPE:STRING': 'Release',
        },
        'debug': {
            'CMAKE_BUILD_TYPE:STRING': 'Debug',
            'PARAVIEW_COLLABORATION_TESTING:BOOL': 'OFF',
        },
    },
}
OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'python': {
        'PARAVIEW_ENABLE_PYTHON:BOOL': ('OFF', 'ON'),
        'VTK_WRAP_PYTHON:BOOL': ('OFF', 'ON'),
    },
    'tcl': {
        'VTK_WRAP_TCL:BOOL': ('OFF', 'ON'),
    },
    'java': {
        'VTK_WRAP_JAVA:BOOL': ('OFF', 'ON'),
    },
    'kits': {
        'VTK_ENABLE_KITS:BOOL': ('OFF', 'ON'),
    },
    'gui': {
        'PARAVIEW_BUILD_QT_GUI:BOOL': ('OFF', 'ON'),
    },
    'mpi': {
        'PARAVIEW_USE_MPI:BOOL': ('OFF', 'ON'),
    },
    'qt5': {
        'PARAVIEW_QT_VERSION:STRING': ('4', '5'),
    },
    'unified': {
        'PARAVIEW_USE_UNIFIED_BINDINGS:BOOL': ('OFF', 'ON'),
    },
    'opengl2': {
        'VTK_RENDERING_BACKEND:STRING': ('OpenGL', 'OpenGL2'),
        # TODO - These plugins don't work with OpenGL2 and are
        #        enabled by default
        'PARAVIEW_BUILD_PLUGIN_PointSprite:BOOL': ('TRUE', 'FALSE'),
        'PARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL': ('TRUE', 'FALSE'),
        'PARAVIEW_BUILD_PLUGIN_SciberQuestToolKit:BOOL': ('TRUE', 'FALSE'),
    },
    'icc': {},
    'vs': {},
    '32bit': {},
}
