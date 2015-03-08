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
        'win32' : {},
        'win64' : {},
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
    'superbuild': {
    }
}
