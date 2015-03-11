__all__ = [
    'NAME',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'vtk'

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
    'mpi': {
        'VTK_Group_MPI:BOOL': ('OFF', 'ON'),
    },
    'qt': {
        'VTK_Group_Qt:STRING': ('OFF', 'ON'),
    },
    'qt5': {
        'VTK_QT_VERSION:STRING': ('4', '5'),
    },
    'opengl2': {
        'VTK_RENDERING_BACKEND:STRING': ('OpenGL', 'OpenGL2'),
    },
    'icc': {},
    'vs': {},
}
