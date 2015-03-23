__all__ = [
    'NAME',
    'OPTIONS',
    'OPTIONORDER',
    'FEATURES',
]

NAME = 'vtksuperbuild'

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
    },
    'buildtype': {
        'release': {
            'CMAKE_BUILD_TYPE:STRING': 'Release',
        },
    },
}

OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'superbuild': {},
    'osx10.7': {},
    '32bit': {},
    '64bit': {},
}
