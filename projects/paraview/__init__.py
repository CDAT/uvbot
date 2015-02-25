__all__ = [
    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

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
        'PARAVIEW_QT_VERSION:STRING': ('5', '4'),
    },
    'unified': {
        'PARAVIEW_USE_UNIFIED_BINDINGS:BOOL': ('OFF', 'ON'),
    },
    'icc': {
    },
}
